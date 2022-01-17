-- les scripts de création des tables
create table PARCOURS(
	codeParc varchar(5) not null,
	libParc varchar(50) not null
);


alter table PARCOURS add constraint PK_PARCOURS primary key(codeParc);

create table NIVEAU(
	codeNiv serial not null,
	libNiv varchar(50) not null,
	nbModules int default 0,
	codeParc varchar(5) not null
);

alter table NIVEAU add constraint FK_NIVEAU_PARCOURS foreign key(codeParc) references PARCOURS(codeParc);
alter table NIVEAU add constraint PK_NIVEAU primary key(codeNiv);

create table ETUDIANT(
	numEtu serial not null,
	nomEtu varchar(10) not null,
	prenomEtu varchar(20) not null,
	sexe char(1) not null check(sexe in ('M','F')),
	dateNaissance date not null,
	codeParc varchar(5) not null
);

alter table ETUDIANT add constraint PK_ETUDIANT primary key(numEtu);
alter table ETUDIANT add constraint FK_ETUDIANT_PARCOURS foreign key(codeParc) references PARCOURS(codeParc);




create table INSCRIRE(
	codeIns serial not null,
	numEtu serial not null,
	codeNiv serial not null,
	anneeIns int default date_part('year', now())
);

alter table INSCRIRE add constraint FK_INSCIRE_ETUDIANT foreign key(numEtu) references ETUDIANT(numEtu);
alter table INSCRIRE add constraint FK_INSCRIRE_NIVEAU foreign key(codeNiv) references NIVEAU(codeNiv);
alter table INSCRIRE add constraint PK_INSCRIRE primary key(codeIns);

create table ENSEIGNANT(
	numEns serial not null,
	nomEns varchar(10) not null,
	prenomEns varchar(20) not null,
	grade varchar(15) not null,
	anneePriseFonct int default date_part('year', now())
);

alter table ENSEIGNANT add constraint PK_ENSEIGNANT primary key(numEns);

create table CLASSE(
	codeClass varchar(5) not null,
	libClass varchar(20) not null,
	capacite int not null
);

alter table CLASSE add constraint PK_CLASSE primary key(codeClass);

create table EVALUATION(
	codeEval varchar(15) not null,
	libEval varchar(25) not null,
	pourcentage real not null check(pourcentage between 0 and 100)
);

alter table EVALUATION add constraint PK_EVALUATION primary key(codeEval);


create table MODULE(
	codeMod varchar(10) not null,
	libMod varchar(20),
	nbCredit int not null,
	est_requis boolean ,
	codeNiv serial not null,
	anneeCreation int default date_part('year', now())
);

alter table MODULE add constraint FK_MODULE_NIVEAU foreign key(codeNiv) references NIVEAU(codeNiv);
alter table MODULE add constraint PK_MODULE primary key(codeMod);

create table MODULES_PREREQUIS(
	codePrerequis varchar(10) not null,
	codeMod varchar(10) not null
);

alter table MODULES_PREREQUIS add constraint FK_MODULES_PREREQUIS_MODULE foreign key(codeMod) references MODULE(codeMod);
alter table MODULES_PREREQUIS add constraint PK_MODULES_PREREQUIS primary key(codePrerequis);





create table DISPENSER(
	codeDisp serial not null,
	codeMod varchar(10) not null,
	codeClass varchar(5) not null,
	numEns serial not null,
	anneeDisp int default date_part('year', now())
);

alter table DISPENSER add constraint FK_DISPENSER_MODULES foreign key(codeMod) references MODULE(codeMod);
alter table DISPENSER add constraint FK_DISPENSER_CLASSE foreign key(codeClass) references CLASSE(codeClass);
alter table DISPENSER add constraint FK_DISPENSER_ENSEIGNANT foreign key(numEns) references ENSEIGNANT(numEns);
alter table DISPENSER add constraint PK_DISPENSER primary key(codeDisp);

create table MODULE_EVAL(
	dateEval date not null,
	note real not null check(note between 0 and 20 ),
	valide boolean,
	codeMod varchar(10) not null,
	numEtu serial not null,
	codeEval varchar(15) not null
);

alter table MODULE_EVAL add constraint FK_MODULE_EVAL_MODULES foreign key(codeMod) references MODULE(codeMod);
alter table MODULE_EVAL add constraint FK_MODULE_EVAL_EVALUATION foreign key(codeEval) references EVALUATION(codeEval);
alter table MODULE_EVAL add constraint FK_NOTER_ETUDIANT foreign key(numEtu) references ETUDIANT(numEtu);
alter table MODULE_EVAL add constraint PK_MODULE_EVALUATION primary key(codeMod, codeEval);






-- Vérifier qu'un étudiant ait au moins 17 ans et au plus 23 ans à sa première inscription (inscription au niveau 1);
create or replace function Function_Verification_Age()
returns trigger
language plpgsql
as  
$$
declare 
age integer;
begin
	-- récupérer l'âge de l'étudiant
	select (date_part('year', now())-date_part('year', "dateNaissance")) into age from public."ETUDIANT";
	
	raise notice 'age : %', age;
	
	if age not between 17 and 23 then
		raise exception 'Un étudiant doit avoir au minimum 17ans et au maximum 23 ans à sa 1ère inscription(inscription au niveau 1)';
	end if;
	
	return new;
end;
$$


create or replace trigger TG_verification_Age
after insert
on public."ETUDIANT"
for each row
execute procedure Function_Verification_Age();



-- Ecrire un trigger pour faire la mise à jour automatique du nombre total de modules pour l’année académique concernée pour un niveau donné;
create or replace function Function_MAG_NbModules_After_Insert()
returns trigger
language plpgsql
as  
$$
declare
nbMod integer := 0;
niv integer;
begin
	select new."codeNiv" into niv from public."MODULE";
	
	select count("codeMod") into nbMod from public."MODULE" M
	join public."NIVEAU" N on M."codeNiv" = N."codeNiv"
	where M."annneeCreation" = date_part('year',now()) and M."codeNiv" = niv;
	
	raise notice 'nb : %',nbMod;
	raise notice 'niv : %',niv;
	
	update public."NIVEAU" set "nbModules" = nbMod where "codeNiv" = niv;
	
	return new;

end;
$$

create or replace trigger TG_MAG_NbModules_After_Insert
after insert 
on public."MODULE"
for each row
execute procedure Function_MAG_NbModules_After_Insert();



-- Toute note validée par le directeur académique ne peut être modifiée que par ce dernier seul;
create or replace function Function_Control_Note_Update()
returns trigger
language plpgsql
as  
$$
declare
user_name varchar;
groupe varchar;
begin
	select username into user_name from public.auth_user
    where last_login = (select max(last_login) from public.auth_user);

    select ag.name into groupe from public.auth_user au
    join public.auth_user_groups aug
    on au.id=aug.user_id
    join public.auth_group ag
    on aug.group_id=ag.id where au.username = user_name; 

    if groupe != 'Directeur' then
        raise exception 'Vous ne pouvez pas réaliser cette action. Privilèges inssuffisants!!!';
    end if;
	
	return new;

end;
$$

create or replace trigger TG_Control_Note_Update
before update
on public."NOTER"
for each row
execute procedure Function_Control_Note_Update()

/*
Un enseignant ne doit consulter, saisir et modifier que les notes des étudiants pour les modules 
qu'il dispense dans une classe dans laquelle il intervient pour une année académique en cours. 
Mais, il peut consulter les notes de tous les étudiants d'une année académique antérieure;
*/

create or replace function Function_Control_Enseignant_Note_Update()
returns trigger
language plpgsql
as  
$$
declare
user_name varchar;
groupe varchar;
annee integer;
begin
	select username into user_name from public.auth_user
    where last_login = (select max(last_login) from public.auth_user);

    select ag.name into groupe from public.auth_user au
    join public.auth_user_groups aug
    on au.id=aug.user_id
    join public.auth_group ag
    on aug.group_id=ag.id where au.username = user_name; 

    select anneeDisp into annee from DISPENSER d
    join ENSEIGNANT e on d.numEns = e.numEns
    where e.nomEns=user_name;

    if groupe='Enseignant' and annee=date_part('year', now()) then
        raise exception 'Vous ne pouvez consulter que les notes des étudiants pour lesquels vous dispnser des cours!!';
    end if;
	
	return new;

end;
$$


create or replace trigger TG_Control_Enseignant_Note_Update
before update
on public."NOTER"
for each row
execute procedure Function_Control_Enseignant_Note_Update()


-- Le directeur académique et le chargé de la scolarité peuvent consulter les notes de tous les étudiants et pour toutes années académiques;

create or replace function Function_Control_Enseignant_Note_Consult()
returns trigger
language plpgsql
as  
$$
declare
user_name varchar;
groupe varchar;
annee integer;
begin
	select username into user_name from public.auth_user
    where last_login = (select max(last_login) from public.auth_user);

    select ag.name into groupe from public.auth_user au
    join public.auth_user_groups aug
    on au.id=aug.user_id
    join public.auth_group ag
    on aug.group_id=ag.id where au.username = user_name; 

    select anneeDisp into annee from DISPENSER d
    join ENSEIGNANT e on d.numEns = e.numEns
    where e.nomEns=user_name;

    if groupe not in ('Directeur', 'Chargé d la scolarité') then
        raise exception 'Acion non autorisée!!';
    end if;
	
	return new;

end;
$$

create or replace trigger TG_Control_Enseignant_Note_Consult
before update
on public."NOTER"
for each row
execute procedure Function_Control_Enseignant_Note_Consult()



/* Un niveau est validé par un étudiant si tous les modules inscrits à ce niveau sont validés par l'étudiant.
 Pour cela, on vous demande d'écrire la fonction qui permet de savoir si un étudiant a validé un niveau donné;
 */


create or replace procedure Function_valider(matricule integer, codeNiv integer)
language plpgsql
as
$$
declare
moy real; 
begin
	select AVG(note*pourcentage) into moy from public."NOTER" N
	join public."EVALUATION" E on E."codeEval" = N."codeEval"
	JOIN public."ETUDIANT" ET ON ET."numEtu" = N."numEtu"
	JOIN public."MODULE" M ON M."codeMod" = N."codeMod"
	where M."codeNiv" = codeNiv and ET."numEtu" = matricule;
	if moy >= 10 then
		raise notice 'Admis!';
		insert into public."RESULTAT"("numEtu", decision)
		values(matricule, 'Admis');
	else
		raise notice 'Echoué!';
		insert into public."RESULTAT"("numEtu", decision)
		values(matricule, 'Echoué');
	end if;
end;
$$

call Function_valider(1,2);
