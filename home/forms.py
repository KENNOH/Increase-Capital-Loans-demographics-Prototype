from django import forms


class UploadFileForm(forms.Form):
    files = forms.FileField(label="Upload excel file:", required=True, widget=forms.ClearableFileInput(
        attrs={'class': 'form-control', 'multiple': "false", 'name': 'file', 'placeholder': 'Upload excel'}))
