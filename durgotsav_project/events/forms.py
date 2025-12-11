from django import forms
from .models import EventRegistration

# Country codes with their validation patterns
COUNTRY_CODES = [
    ('+91', '🇮🇳 India +91'),
    ('+1', '🇺🇸 USA +1'),
    ('+44', '🇬🇧 UK +44'),
    ('+61', '🇦🇺 Australia +61'),
    ('+65', '🇸🇬 Singapore +65'),
    ('+971', '🇦🇪 UAE +971'),
    ('+86', '🇨🇳 China +86'),
    ('+81', '🇯🇵 Japan +81'),
    ('+82', '🇰🇷 South Korea +82'),
    ('+60', '🇲🇾 Malaysia +60'),
    ('+66', '🇹🇭 Thailand +66'),
    ('+92', '🇵🇰 Pakistan +92'),
    ('+94', '🇱🇰 Sri Lanka +94'),
    ('+880', '🇧🇩 Bangladesh +880'),
    ('+977', '🇳🇵 Nepal +977'),
]

class RegistrationForm(forms.ModelForm):
    country_code = forms.ChoiceField(
        choices=COUNTRY_CODES,
        initial='+91',
        widget=forms.Select(attrs={
            'class': 'form-select country-code-select',
            'id': 'country_code',
            'required': True
        })
    )
    
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control phone-number-input',
            'placeholder': 'Enter phone number',
            'required': True,
            'id': 'phone_number'
        })
    )
    
    selected_events = forms.JSONField(
        widget=forms.HiddenInput(attrs={
            'id': 'selected_events'
        }),
        required=False
    )

    class Meta:
        model = EventRegistration
        fields = ['name', 'country_code', 'phone_number', 'email', 'selected_events']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        country_code = self.data.get('country_code', '+91')
        
        # Remove any spaces, dashes, etc.
        phone_number = ''.join(filter(str.isdigit, phone_number))
        
        # Check if phone number is empty
        if not phone_number:
            raise forms.ValidationError("Phone number is required.")
        
        # Check expected length for the country
        expected_length = 10  # Default length
        if len(phone_number) != expected_length:
            raise forms.ValidationError(
                f"Phone number must be exactly {expected_length} digits."
            )
        
        # Country-specific validation
        if country_code == '+91':  # India
            if not phone_number.startswith(('6', '7', '8', '9')):
                raise forms.ValidationError(
                    "Indian mobile numbers must start with 6, 7, 8, or 9."
                )
        
        return phone_number