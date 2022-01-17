from django.db import models
import datetime

#pip install psycopg2
#pip install -U django-jazzmin

class Parcours(models.Model):
    codeParc = models.CharField(max_length=5, primary_key=True)
    libParc = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f"{self.libParc}"

    class Meta:
        db_table = 'PARCOURS'


class Niveau(models.Model):
    codeNiv = models.BigAutoField(primary_key=True)
    libNiv = models.CharField(max_length=20, blank=False)
    nbModules = models.IntegerField(default=0)
    codeParc = models.ForeignKey(Parcours, on_delete=models.RESTRICT, blank=False, db_column='codeParc')

    def __str__(self):
        return f"{self.libNiv}"

    class Meta:
        db_table = 'NIVEAU'




class Etudiant(models.Model):
    SEXE_CHOICES = (
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    )
    numEtu = models.BigAutoField(primary_key=True)
    nomEtu = models.CharField(max_length=10, blank=False)
    prenomEtu = models.CharField(max_length=50, blank=False)
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES)
    dateNaissance = models.DateField(blank=False)
    codeParc = models.ForeignKey(Parcours, on_delete=models.RESTRICT, blank=False, db_column='codeParc')


    def __str__(self):
        return f"{self.nomEtu}, {self.prenomEtu}"

    class Meta:
        db_table = 'ETUDIANT'



class Inscrire(models.Model):
    date = datetime.datetime.now()

    codeIns= models.BigAutoField(primary_key=True)
    numEtu = models.ForeignKey(Etudiant, on_delete=models.RESTRICT, blank=False, db_column='numEtu')
    codeNiv = models.ForeignKey(Niveau, on_delete=models.RESTRICT, blank=False, db_column='codeNiv')
    annneeIns = models.IntegerField(default=date.year)

    def __str__(self):
        return f"{self.codeIns}, {self.numEtu}, {self.codeNiv}"

    class Meta:
        db_table = 'INSCRIRE'


class Enseignant(models.Model):
    date = datetime.datetime.now()

    numEns = models.BigAutoField(primary_key=True)
    nomEns = models.CharField(max_length=10, blank=False)
    prenomEns = models.CharField(max_length=20, blank=False)
    grade = models.CharField(max_length=15, blank=False)
    annneePriseFonct = models.IntegerField(default=date.year)

    def __str__(self):
        return f"{self.nomEns}"

    class Meta:
        db_table = 'ENSEIGNANT'


class Classe(models.Model):
    codeClass = models.CharField(max_length=5, blank=False, primary_key=True)
    libClass = models.CharField(max_length=10, blank=False)
    capacite = models.IntegerField()

    def __str__(self):
        return f"{self.libClass}"

    class Meta:
        db_table = 'CLASSE'


class Evaluation(models.Model):
    codeEval = models.CharField(max_length=15, blank=False, primary_key=True)
    libEval = models.CharField(max_length=20, blank=False)
    pourcentage = models.IntegerField(blank=False, default=range(0,100))

    def __str__(self):
        return f"{self.libEval}"

    class Meta:
        db_table = 'EVALUATION'



class Module(models.Model):
    date = datetime.datetime.now()

    codeMod = models.CharField(max_length=10, blank=False, primary_key=True)
    libMod = models.CharField(max_length=20, blank=False)
    nbCredit = models.IntegerField(blank=False)
    est_requis = models.BooleanField(blank=False)
    codeNiv = models.ForeignKey(Niveau, on_delete=models.RESTRICT, blank=False, db_column='codeNiv')
    annneeCreation = models.IntegerField(default=date.year)

    def __str__(self):
        return f"{self.libMod}"


    class Meta:
        db_table = 'MODULE'


class ModulePrerequis(models.Model):
    idPre = models.BigAutoField(primary_key=True)
    codePrerequis = models.ForeignKey(Module, on_delete=models.RESTRICT, blank=False, related_name='codePre', db_column='codePrerequis')
    codeMod = models.ForeignKey(Module, on_delete=models.RESTRICT, blank=False, related_name='codeModule', db_column='codeMod')

    def __str__(self):
        return f"{self.codePrerequis}"


    class Meta:
        db_table = 'MODULES_PREREQUIS'


class Dispenser(models.Model):
    date = datetime.datetime.now()

    codeDisp = models.BigAutoField(primary_key=True)
    codeMod = models.ForeignKey(Module, on_delete=models.RESTRICT, blank=False, db_column='codeMod')
    codeclass = models.ForeignKey(Classe, on_delete=models.RESTRICT, blank=False, db_column='codeClass')
    numEns = models.ForeignKey(Enseignant, on_delete=models.RESTRICT, blank=False, db_column='numEns')
    annneeDisp = models.IntegerField(default=date.year)

    def __str__(self):
        return f"{self.codeDisp}, {self.codeMod}, {self.codeclass}, {self.numEns}, {self.annneeDisp}"


    class Meta:
        db_table = 'DISPENSER'



class Noter(models.Model):
    idNote = models.BigAutoField(primary_key=True)
    numEtu = models.ForeignKey(Etudiant, on_delete=models.RESTRICT, blank=False, db_column='numEtu')
    dateEval = models.DateField(blank=False)
    note = models.FloatField(blank=False)
    codeMod = models.ForeignKey(Module, on_delete=models.RESTRICT, blank=False, db_column='codeMod')
    codeEval = models.ForeignKey(Evaluation, on_delete=models.RESTRICT, blank=False, db_column='codeEval')


    def __str__(self):
        return f"{self.numEtu}, {self.dateEval}, {self.note}, {self.valide}, {self.codeMod}, {self.codeEval}"
    



    class Meta:
        db_table = 'NOTER'



class Resultat(models.Model):
    idRes = models.BigAutoField(primary_key=True)
    numEtu = models.ForeignKey(Etudiant, on_delete=models.RESTRICT, blank=False, db_column='numEtu')
    decision = models.CharField(blank=False, max_length=10)
    

    def __str__(self):
        return f"{self.numEtu}, {self.decision}"
    



    class Meta:
        db_table = 'RESULTAT'







