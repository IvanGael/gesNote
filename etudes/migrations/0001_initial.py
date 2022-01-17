# Generated by Django 4.0 on 2022-01-12 17:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Classe',
            fields=[
                ('codeClass', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('libClass', models.CharField(max_length=10)),
                ('capacite', models.IntegerField()),
            ],
            options={
                'db_table': 'CLASSE',
            },
        ),
        migrations.CreateModel(
            name='Enseignant',
            fields=[
                ('numEns', models.BigAutoField(primary_key=True, serialize=False)),
                ('nomEns', models.CharField(max_length=10)),
                ('prenomEns', models.CharField(max_length=20)),
                ('grade', models.CharField(max_length=15)),
                ('annneePriseFonct', models.IntegerField(default=2022)),
            ],
            options={
                'db_table': 'ENSEIGNANT',
            },
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('numEtu', models.BigAutoField(primary_key=True, serialize=False)),
                ('nomEtu', models.CharField(max_length=10)),
                ('prenomEtu', models.CharField(max_length=50)),
                ('sexe', models.CharField(choices=[('M', 'Masculin'), ('F', 'Féminin')], max_length=1)),
                ('dateNaissance', models.DateField()),
            ],
            options={
                'db_table': 'ETUDIANT',
            },
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('codeEval', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('libEval', models.CharField(max_length=20)),
                ('pourcentage', models.IntegerField(default=range(0, 100))),
            ],
            options={
                'db_table': 'EVALUATION',
            },
        ),
        migrations.CreateModel(
            name='Module',
            fields=[
                ('codeMod', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('libMod', models.CharField(max_length=20)),
                ('nbCredit', models.IntegerField()),
                ('est_requis', models.BooleanField()),
                ('annneeCreation', models.IntegerField(default=2022)),
            ],
            options={
                'db_table': 'MODULE',
            },
        ),
        migrations.CreateModel(
            name='Parcours',
            fields=[
                ('codeParc', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('libParc', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'PARCOURS',
            },
        ),
        migrations.CreateModel(
            name='Noter',
            fields=[
                ('idNote', models.BigAutoField(primary_key=True, serialize=False)),
                ('dateEval', models.DateField()),
                ('note', models.FloatField()),
                ('valide', models.BooleanField()),
                ('codeEval', models.ForeignKey(db_column='codeEval', on_delete=django.db.models.deletion.RESTRICT, to='etudes.evaluation')),
                ('codeMod', models.ForeignKey(db_column='codeMod', on_delete=django.db.models.deletion.RESTRICT, to='etudes.module')),
                ('numEtu', models.ForeignKey(db_column='numEtu', on_delete=django.db.models.deletion.RESTRICT, to='etudes.etudiant')),
            ],
            options={
                'db_table': 'NOTER',
            },
        ),
        migrations.CreateModel(
            name='Niveau',
            fields=[
                ('codeNiv', models.BigAutoField(primary_key=True, serialize=False)),
                ('libNiv', models.CharField(max_length=20)),
                ('nbModules', models.IntegerField(default=0)),
                ('codeParc', models.ForeignKey(db_column='codeParc', on_delete=django.db.models.deletion.RESTRICT, to='etudes.parcours')),
            ],
            options={
                'db_table': 'NIVEAU',
            },
        ),
        migrations.CreateModel(
            name='ModulePrerequis',
            fields=[
                ('idPre', models.BigAutoField(primary_key=True, serialize=False)),
                ('codeMod', models.ForeignKey(db_column='codeMod', on_delete=django.db.models.deletion.RESTRICT, related_name='codeModule', to='etudes.module')),
                ('codePrerequis', models.ForeignKey(db_column='codePrerequis', on_delete=django.db.models.deletion.RESTRICT, related_name='codePre', to='etudes.module')),
            ],
            options={
                'db_table': 'MODULES_PREREQUIS',
            },
        ),
        migrations.AddField(
            model_name='module',
            name='codeNiv',
            field=models.ForeignKey(db_column='codeNiv', on_delete=django.db.models.deletion.RESTRICT, to='etudes.niveau'),
        ),
        migrations.CreateModel(
            name='Inscrire',
            fields=[
                ('codeIns', models.BigAutoField(primary_key=True, serialize=False)),
                ('annneeIns', models.IntegerField(default=2022)),
                ('codeNiv', models.ForeignKey(db_column='codeNiv', on_delete=django.db.models.deletion.RESTRICT, to='etudes.niveau')),
                ('numEtu', models.ForeignKey(db_column='numEtu', on_delete=django.db.models.deletion.RESTRICT, to='etudes.etudiant')),
            ],
            options={
                'db_table': 'INSCRIRE',
            },
        ),
        migrations.AddField(
            model_name='etudiant',
            name='codeParc',
            field=models.ForeignKey(db_column='codeParc', on_delete=django.db.models.deletion.RESTRICT, to='etudes.parcours'),
        ),
        migrations.CreateModel(
            name='Dispenser',
            fields=[
                ('codeDisp', models.BigAutoField(primary_key=True, serialize=False)),
                ('annneeDisp', models.IntegerField(default=2022)),
                ('codeMod', models.ForeignKey(db_column='codeMod', on_delete=django.db.models.deletion.RESTRICT, to='etudes.module')),
                ('codeclass', models.ForeignKey(db_column='codeClass', on_delete=django.db.models.deletion.RESTRICT, to='etudes.classe')),
                ('numEns', models.ForeignKey(db_column='numEns', on_delete=django.db.models.deletion.RESTRICT, to='etudes.enseignant')),
            ],
            options={
                'db_table': 'DISPENSER',
            },
        ),
    ]
