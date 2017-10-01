from django import forms
from rcexp.models import Exp_Info, User_Route_Choice

# class NewExp(forms.Form):
#     agree_except = forms.BooleanField(required=True)

class Game_Info(forms.Form):
    user_num = forms.IntegerField(required=False, min_value=1)
    time_interval = forms.IntegerField(required=False, min_value=1)
    def clean(self):
        cleaned_data = super(Game_Info, self).clean()
        user_num = cleaned_data.get("user_num")
        time_interval = cleaned_data.get("time_interval")
        try: 
            int(user_num)
        except:
            raise forms.ValidationError("Please input a positive integer")
        try: 
            int(time_interval)
        except:
            raise forms.ValidationError("Please input a positive integer")
        # print(user_num, time_interval)
        return self.cleaned_data

class Route_Choice(forms.Form):
    user_choice = (('1', 'Top',), ('2', 'Middle',), ('3', 'Bottom',))
    route_choice = forms.ChoiceField(widget=forms.RadioSelect(), choices=user_choice, required=False) # required=True
    exp_id = forms.CharField(widget=forms.HiddenInput())
    user_id = forms.CharField(widget=forms.HiddenInput())
    exp_day = forms.CharField(widget=forms.HiddenInput())
    # def clean(self):
    #     cleaned_data = super(Route_Choice, self).clean()
    #     user_id = cleaned_data.get("user_id")
    #     route_choice = cleaned_data.get("route_choice")
    #     exp_id = cleaned_data.get("exp_id")
    #     exp_day = int(cleaned_data.get("exp_day"))
    #     print('route_choice is ', route_choice)
    #     if user_id != 'Admin':
    #         if not route_choice:
    #             raise forms.ValidationError("Please choose a route")
    #         else:
    #             p =  Exp_Info.objects.get(exp_id=exp_id)
    #             current_day = int(p.exp_day)
    #             if exp_day > current_day:
    #                     raise forms.ValidationError("The day is not comming yet, please choose again")
    #             elif exp_day < current_day:
    #                     raise forms.ValidationError("The day has expired, please choose again")
    #             try:
    #                 p = User_Route_Choice.objects.get(exp_id=exp_id, user_id=user_id, exp_day=exp_day)
    #             except:
    #                 pass
    #             else:
    #                 raise forms.ValidationError("Repeated submission")
    #     return self.cleaned_data




    # def clean_route_choice(self):
    #     user_id = self.cleaned_data['user_id']
    #     route_choice = self.cleaned_data['route_choice']
    #     if user_id != 'Admin' and not route_choice:
    #         raise forms.ValidationError("Please choose a route")
    #     return route_choice


# class ContactForm(forms.Form):
#     subject = forms.CharField(max_length=100)
#     email = forms.EmailField(required=False)
#     message = forms.CharField(widget=forms.Textarea)

#     def clean_message(self):
#         message = self.cleaned_data['message']
#         num_words = len(message.split())
#         if num_words < 4:
#             raise forms.ValidationError("Not enough words!")
#         return message