from django import forms

from .models import Post, Follow

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('user_id', 'body','username')
        widgets = {'user_id': forms.HiddenInput(), 'username': forms.HiddenInput(), 'body': forms.TextInput(
				attrs={
					'class': 'form_body',
                    'id':'form_body'
					})
        }


class FollowForm(forms.ModelForm):
    
    class Meta:
        model = Follow
        fields = ('follower_id', 'following_id','following_posts')
        widgets = {'follower_id': forms.HiddenInput(), 'following_id': forms.HiddenInput(), 'following_posts':forms.CheckboxSelectMultiple()}
