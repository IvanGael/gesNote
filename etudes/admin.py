from django.contrib import admin
from .models import *

admin.site.site_title='Gestion des notes'

admin.site.site_header='GesNote'


class ParcoursAdmin(admin.ModelAdmin):
    fields = ('codeParc', 'libParc')
    list_display = ('codeParc', 'libParc')


class NiveauAdmin(admin.ModelAdmin):
    fields = ('libNiv', 'nbModules', 'codeParc')
    list_display = ( 'libNiv', 'nbModules', 'codeParc')


class EtudiantAdmin(admin.ModelAdmin):
    fields = ('nomEtu', 'prenomEtu', 'sexe','dateNaissance', 'codeParc')
    list_display = ('nomEtu', 'prenomEtu', 'sexe','dateNaissance', 'codeParc')

class InscrireAdmin(admin.ModelAdmin):
    fields = ('numEtu', 'codeNiv', 'annneeIns')
    list_display = ('numEtu', 'codeNiv', 'annneeIns')

class EnseignantAdmin(admin.ModelAdmin):
    fields = ('nomEns', 'prenomEns', 'grade','annneePriseFonct')
    list_display = ('nomEns', 'prenomEns', 'grade','annneePriseFonct')


class ClasseAdmin(admin.ModelAdmin):
    fields = ('codeClass', 'libClass', 'capacite')
    list_display = ('codeClass', 'libClass', 'capacite')

class EvaluationAdmin(admin.ModelAdmin):
    fields = ('codeEval', 'libEval', 'pourcentage')
    list_display = ('codeEval', 'libEval', 'pourcentage')

class ModuleAdmin(admin.ModelAdmin):
    fields = ('codeMod', 'libMod', 'nbCredit', 'est_requis', 'codeNiv', 'annneeCreation')
    list_display = ('codeMod', 'libMod', 'nbCredit', 'est_requis', 'codeNiv', 'annneeCreation')

class ModulePrerequisAdmin(admin.ModelAdmin):
    fields = ('codeMod', 'codePrerequis')
    list_display = ('codeMod', 'codePrerequis')

class DispenserAdmin(admin.ModelAdmin):
    fields = ('codeMod', 'codeclass','numEns', 'annneeDisp')
    list_display = ('codeMod', 'codeclass','numEns', 'annneeDisp')

class NoterAdmin(admin.ModelAdmin):
    fields = ('numEtu', 'dateEval','note', 'codeMod', 'codeEval')
    list_display = ('numEtu', 'dateEval','note', 'codeMod', 'codeEval')

class ResultatAdmin(admin.ModelAdmin):
    fields = ('numEtu', 'decision')
    list_display = ('numEtu', 'decision')



admin.site.register(Parcours, ParcoursAdmin)
admin.site.register(Niveau, NiveauAdmin)
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.register(Inscrire, InscrireAdmin)
admin.site.register(Enseignant, EnseignantAdmin)
admin.site.register(Classe, ClasseAdmin)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(ModulePrerequis, ModulePrerequisAdmin)
admin.site.register(Dispenser, DispenserAdmin)
admin.site.register(Noter, NoterAdmin)
admin.site.register(Resultat, ResultatAdmin)
