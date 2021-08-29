from django import forms
from .models import Post, Comment, Reply

class PostModelForm(forms.ModelForm):
	content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
	
	class Meta:
		model = Post
		fields = ('content', 'image')

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)

class ReplyModelForm(forms.ModelForm):
	body = forms.CharField(label='Reply', 
                            widget=forms.TextInput(attrs={'placeholder': 'Add a Reply...'}))
	class Meta:
		model = Reply
		fields = ('body',)