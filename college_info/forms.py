from django import forms
from .models import Assignment,BatchAttendance
from functools import partial

DateInput =partial(forms.DateInput,{'class':'datepicker'})

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = Assignment
        fields = ['teach','title','message','submission_date','doc']
        labels={
            'teach':'Course',
            'submission_date':'Submission Date',
            'doc':'Attach Assignment'
        }
        widgets = {
            'submission_date': DateInput()

        }

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = BatchAttendance
        fields = ['teach','date']
        labels={
            'teach':'Course',
            'date':'Date'
        }
        widgets={
            'date':DateInput()

        }
