# -*- coding: utf-8 -*-
from django.db import models
from gp_utils.common.models import Member, Board

# Create your models here.
class FeedbackSet(models.Model):
    date = models.DateField()
    finished = models.BooleanField()
    #TODO: Implement data exporting to pretty graphs
    class Meta:
        permissions = (
            #Mainly for HR employees
            ("view_other_feedbacks", "Can view reports for every member."),
        )
    def __unicode__(self):
        return str(self.date)
    
class FeedbackMember(models.Model):
    evaluator = models.ForeignKey(Member, related_name='evaluator')
    evaluee = models.ForeignKey(Member, related_name='evaluee')
    superset = models.ForeignKey(FeedbackSet)    

    commitment = models.IntegerField('Comprometimento')
    teamwork = models.IntegerField('Trabalho em equipe')
    proactivity = models.IntegerField('Proatividade')
    
    #This is the list of criteria. Include all of the evaluation criteria here to use them in the evaluation framework
    CRITERIA = (commitment, teamwork, proactivity, )
    def __unicode__(self):
        return str(self.superset) + ' - De ' + str(self.evaluator) + ' para ' + str(self.evaluee)