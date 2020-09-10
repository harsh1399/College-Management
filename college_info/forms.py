from django import forms
from .models import Assignment

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['teach','title','message','submission_date','doc']
        labels={
            'teach':'Course',
            'submission_date':'Submission Date',
            'doc':'Attach Assignment'
        }