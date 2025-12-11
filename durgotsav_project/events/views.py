from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from .models import EventRegistration, EventDay
from .forms import RegistrationForm
from datetime import date, timedelta
import json

def calendar_view(request):
    # Festival schedule with detailed events
    festival_schedule = {
        'Day 1 - Shashthi (The Awakening & Welcome)': [
            ('9:00 AM – 10:30 AM', 'Bodhon Ceremony – Interactive Ritual'),
            ('10:45 AM – 12:15 PM', 'Shankh Blowing Competition'),
            ('12:30 PM – 1:30 PM', 'Alpona / Rangoli Design Workshop'),
            ('2:00 PM – 3:00 PM', 'AR Immersive Zones Walkthrough'),
            ('3:00 PM – 4:30 PM', 'Cultural Context Masterclass – "Durga Through Time"'),
            ('4:30 PM – 5:30 PM', 'Regional Festival Micro-Exhibition Setup'),
            ('6:00 PM – 7:00 PM', 'Opening Ceremony & Welcome Performance'),
            ('7:15 PM – 8:15 PM', 'Dhunuchi Naach Flash Mob & Participation'),
            ('7:00 PM – 11:00 PM', 'Night Food Trail & Culinary Experiences'),
            ('8:00 PM – 10:00 PM', 'Luxury Fashion Lounge & Styling Studio'),
            ('9:00 PM – 12:00 AM', 'Indie Music & Fusion Concert Night'),
        ],

        'Day 2 - Saptami (The Creative Spirit & Expression)': [
            ('9:00 AM – 11:00 AM', 'Eco-Friendly Idol Making Masterclass'),
            ('11:15 AM – 1:00 PM', 'Blooming 108 Lotuses Installation Challenge'),
            ('12:00 PM – 1:00 PM', 'Kannada Classical Dance Masterclass'),
            ('2:00 PM – 5:00 PM', 'Regional Festival Comparative Exhibition – Full Experience'),
            ('2:30 PM – 3:30 PM', 'Live Pattachitra & Kalamkari Painting Demonstration'),
            ('4:00 PM – 5:30 PM', 'Traditional Textile Workshop & Fashion Seminar'),
            ('6:00 PM – 7:00 PM', 'Sandhi Puja – The Sacred Transition Ritual'),
            ('7:15 PM – 8:30 PM', 'Kumari Puja Preview & Girl-Child Empowerment Panel'),
            ('8:45 PM – 10:00 PM', 'Fashion Fusion Show – "Saree to Street"'),
            ('10:15 PM – 12:00 AM', 'Comedy & Storytelling Night'),
        ],

        'Day 3 - Ashtami (The Power Day & Spiritual Peak)': [
            ('9:00 AM – 10:30 AM', 'Kumari Puja Ceremony – Full Ritual'),
            ('10:45 AM – 12:00 PM', 'Pushpanjali Mass Participation – Flower Offering'),
            ('12:15 PM – 1:30 PM', 'Women Empowerment & Durga as Feminist Icon Panel'),
            ('2:00 PM – 3:00 PM', 'Weapons & Symbolism Interactive Workshop'),
            ('3:00 PM – 4:30 PM', 'Ashtami Special Bhog Feast & Food Ceremony'),
            ('4:45 PM – 5:45 PM', 'Martial Arts & Power Showcase'),
            ('6:00 PM – 6:30 PM', 'Aarti – Evening Prayer Ceremony'),
            ('6:45 PM – 7:30 PM', 'Pushpanjali Evening Ritual – Second Round'),
            ('7:45 PM – 9:00 PM', 'Ashtami Dhunuchi Naach Competition'),
            ('9:15 PM – 10:30 PM', 'Immersive Theatre – "The Slaying of Mahishasur"'),
            ('10:45 PM – 1:00 AM', 'EDM & Dhak Fusion Late-Night Concert'),
        ],

        'Day 4 - Navami (The Celebration Peak & Joy)': [
            ('9:00 AM – 11:00 AM', 'Sindoor Khela Preview & Photography'),
            ('11:15 AM – 1:00 PM', 'Multi-Regional Dance Battle'),
            ('2:00 PM – 2:45 PM', 'Pushpanjali – Third Ritual Round'),
            ('3:00 PM – 4:30 PM', 'Navami Bhog Feast – Second Service'),
            ('4:00 PM – 5:00 PM', 'Comedy & Satire Theatre Performance'),
            ('6:00 PM – 6:30 PM', 'Aarti – Navami Evening Ceremony'),
            ('6:45 PM – 7:45 PM', 'Navami Special Dhunuchi Naach – Grand Performance'),
            ('8:00 PM – 9:30 PM', 'Film Festival Screening – Indian Cinema Celebrates Durga'),
            ('9:45 PM – 11:00 PM', 'Immersive Light & Sound Show – "Goddess Rising"'),
            ('11:15 PM – 2:00 AM', 'DJ Battle & Late-Night Dance Festival'),
        ],

        'Day 5 - Dashami (The Grand Finale & Farewell)': [
            ('9:00 AM – 11:00 AM', 'Sindoor Khela – The Iconic Ritual'),
            ('11:15 AM – 1:00 PM', 'Immersion Procession & Environmental Awareness Workshop'),
            ('12:00 PM – 12:45 PM', 'Pushpanjali – Final Ritual Round'),
            ('2:00 PM – 4:00 PM', 'Dashami Bhog Feast – Grand Finale Service'),
            ('3:00 PM – 4:00 PM', 'Awards & Recognition Ceremony'),
            ('4:00 PM – 4:30 PM', 'Aarti – Final Daylight Ceremony'),
            ('5:00 PM – 7:00 PM', 'Visarjan Procession – Eco-Friendly Immersion'),
            ('7:00 PM – 8:00 PM', 'Post-Immersion Reflection & Closure Gathering'),
            ('8:00 PM – 9:30 PM', 'Gratitude Feast & Bonfire Celebration'),
            ('9:30 PM – 10:00 PM', 'Closing Ceremony & Digital Fireworks Show'),
        ]
    }

    # Dates for each day
    event_dates = [
        date(2025, 10, 2),
        date(2025, 10, 3),
        date(2025, 10, 4),
        date(2025, 10, 5),
        date(2025, 10, 6)
    ]

    # Combine titles, dates, and schedules
    event_data = []
    for i, (title, schedule) in enumerate(festival_schedule.items()):
        event_data.append((title, event_dates[i], schedule))
    
    return render(request, 'events/calendar.html', {'event_data': event_data})

def day_detail_view(request, day_number):
    festival_schedule = {
        'Day 1 - Shashthi (The Awakening & Welcome)': [
            ('9:00 AM – 10:30 AM', 'Bodhon Ceremony – Interactive Ritual'),
            ('10:45 AM – 12:15 PM', 'Shankh Blowing Competition'),
            ('12:30 PM – 1:30 PM', 'Alpona / Rangoli Design Workshop'),
            ('2:00 PM – 3:00 PM', 'AR Immersive Zones Walkthrough'),
            ('3:00 PM – 4:30 PM', 'Cultural Context Masterclass – "Durga Through Time"'),
            ('4:30 PM – 5:30 PM', 'Regional Festival Micro-Exhibition Setup'),
            ('6:00 PM – 7:00 PM', 'Opening Ceremony & Welcome Performance'),
            ('7:15 PM – 8:15 PM', 'Dhunuchi Naach Flash Mob & Participation'),
            ('7:00 PM – 11:00 PM', 'Night Food Trail & Culinary Experiences'),
            ('8:00 PM – 10:00 PM', 'Luxury Fashion Lounge & Styling Studio'),
            ('9:00 PM – 12:00 AM', 'Indie Music & Fusion Concert Night'),
        ],

        'Day 2 - Saptami (The Creative Spirit & Expression)': [
            ('9:00 AM – 11:00 AM', 'Eco-Friendly Idol Making Masterclass'),
            ('11:15 AM – 1:00 PM', 'Blooming 108 Lotuses Installation Challenge'),
            ('12:00 PM – 1:00 PM', 'Kannada Classical Dance Masterclass'),
            ('2:00 PM – 5:00 PM', 'Regional Festival Comparative Exhibition – Full Experience'),
            ('2:30 PM – 3:30 PM', 'Live Pattachitra & Kalamkari Painting Demonstration'),
            ('4:00 PM – 5:30 PM', 'Traditional Textile Workshop & Fashion Seminar'),
            ('6:00 PM – 7:00 PM', 'Sandhi Puja – The Sacred Transition Ritual'),
            ('7:15 PM – 8:30 PM', 'Kumari Puja Preview & Girl-Child Empowerment Panel'),
            ('8:45 PM – 10:00 PM', 'Fashion Fusion Show – "Saree to Street"'),
            ('10:15 PM – 12:00 AM', 'Comedy & Storytelling Night'),
        ],

        'Day 3 - Ashtami (The Power Day & Spiritual Peak)': [
            ('9:00 AM – 10:30 AM', 'Kumari Puja Ceremony – Full Ritual'),
            ('10:45 AM – 12:00 PM', 'Pushpanjali Mass Participation – Flower Offering'),
            ('12:15 PM – 1:30 PM', 'Women Empowerment & Durga as Feminist Icon Panel'),
            ('2:00 PM – 3:00 PM', 'Weapons & Symbolism Interactive Workshop'),
            ('3:00 PM – 4:30 PM', 'Ashtami Special Bhog Feast & Food Ceremony'),
            ('4:45 PM – 5:45 PM', 'Martial Arts & Power Showcase'),
            ('6:00 PM – 6:30 PM', 'Aarti – Evening Prayer Ceremony'),
            ('6:45 PM – 7:30 PM', 'Pushpanjali Evening Ritual – Second Round'),
            ('7:45 PM – 9:00 PM', 'Ashtami Dhunuchi Naach Competition'),
            ('9:15 PM – 10:30 PM', 'Immersive Theatre – "The Slaying of Mahishasur"'),
            ('10:45 PM – 1:00 AM', 'EDM & Dhak Fusion Late-Night Concert'),
        ],

        'Day 4 - Navami (The Celebration Peak & Joy)': [
            ('9:00 AM – 11:00 AM', 'Sindoor Khela Preview & Photography'),
            ('11:15 AM – 1:00 PM', 'Multi-Regional Dance Battle'),
            ('2:00 PM – 2:45 PM', 'Pushpanjali – Third Ritual Round'),
            ('3:00 PM – 4:30 PM', 'Navami Bhog Feast – Second Service'),
            ('4:00 PM – 5:00 PM', 'Comedy & Satire Theatre Performance'),
            ('6:00 PM – 6:30 PM', 'Aarti – Navami Evening Ceremony'),
            ('6:45 PM – 7:45 PM', 'Navami Special Dhunuchi Naach – Grand Performance'),
            ('8:00 PM – 9:30 PM', 'Film Festival Screening – Indian Cinema Celebrates Durga'),
            ('9:45 PM – 11:00 PM', 'Immersive Light & Sound Show – "Goddess Rising"'),
            ('11:15 PM – 2:00 AM', 'DJ Battle & Late-Night Dance Festival'),
        ],

        'Day 5 - Dashami (The Grand Finale & Farewell)': [
            ('9:00 AM – 11:00 AM', 'Sindoor Khela – The Iconic Ritual'),
            ('11:15 AM – 1:00 PM', 'Immersion Procession & Environmental Awareness Workshop'),
            ('12:00 PM – 12:45 PM', 'Pushpanjali – Final Ritual Round'),
            ('2:00 PM – 4:00 PM', 'Dashami Bhog Feast – Grand Finale Service'),
            ('3:00 PM – 4:00 PM', 'Awards & Recognition Ceremony'),
            ('4:00 PM – 4:30 PM', 'Aarti – Final Daylight Ceremony'),
            ('5:00 PM – 7:00 PM', 'Visarjan Procession – Eco-Friendly Immersion'),
            ('7:00 PM – 8:00 PM', 'Post-Immersion Reflection & Closure Gathering'),
            ('8:00 PM – 9:30 PM', 'Gratitude Feast & Bonfire Celebration'),
            ('9:30 PM – 10:00 PM', 'Closing Ceremony & Digital Fireworks Show'),
        ]
    }

    # Dates for each day
    event_dates = [
        date(2025, 10, 2),
        date(2025, 10, 3),
        date(2025, 10, 4),
        date(2025, 10, 5),
        date(2025, 10, 6)
    ]

    day_titles = list(festival_schedule.keys())
    
    if day_number < 1 or day_number > len(day_titles):
        return redirect('calendar')
    
    day_title = day_titles[day_number - 1]
    day_date = event_dates[day_number - 1]
    day_schedule = festival_schedule[day_title]
    
    return render(request, 'events/day_detail.html', {
        'day_number': day_number,
        'day_title': day_title,
        'day_date': day_date,
        'day_schedule': day_schedule,
    })

def registration_view(request):
    if request.method == 'POST':
        print("=== REGISTRATION DEBUG INFO ===")
        print("POST data:", dict(request.POST))
        print("Selected events raw:", request.POST.get('selected_events'))
        
        # Create a mutable copy of POST data
        post_data = request.POST.copy()
        
        # Get selected events before form validation
        selected_events_json = post_data.get('selected_events', '[]')
        print("Selected events JSON:", selected_events_json)
        
        try:
            selected_events = json.loads(selected_events_json)
            print("Parsed selected events:", selected_events)
            print("Number of selected events:", len(selected_events))
        except json.JSONDecodeError as e:
            print("❌ JSON decode error:", e)
            selected_events = []
        
        # Create form instance
        form = RegistrationForm(post_data)
        
        if form.is_valid():
            # Save the registration first
            registration = form.save(commit=False)
            
            # Manually set the selected_events field
            registration.selected_events = selected_events
            registration.save()
            
            print("✅ Registration saved with selected events:", len(selected_events))
            
            try:
                # Send confirmation email to user
                user_subject = 'Registration Confirmation - Durgotsav 25'
                
                # Build events list for email
                if selected_events:
                    events_list = "\n".join([f"• {event['time']}: {event['name']}" for event in selected_events])
                else:
                    events_list = "• No specific events selected (registered for the day)"
                
                user_message_plain = f"""
Dear {registration.name},

Thank you for registering for Durgotsav 25!

Your Registration Details:
- Name: {registration.name}
- Email: {registration.email}
- Phone: {registration.country_code} {registration.phone_number}

Events You've Registered For:
{events_list}

We look forward to celebrating with you!

Best regards,
Durgotsav 25 Team
"""

                # HTML version for email
                user_message_html = render_to_string('events/email/user_confirmation.html', {
                    'name': registration.name,
                    'email': registration.email,
                    'phone': registration.phone_number,
                    'country_code': registration.country_code,
                    'selected_events': selected_events,
                })

                send_mail(
                    user_subject,
                    user_message_plain,
                    settings.DEFAULT_FROM_EMAIL,
                    [registration.email],
                    fail_silently=False,
                    html_message=user_message_html
                )

                # Send notification email to owner
                owner_subject = f'New Registration: {registration.name}'
                owner_message_plain = f"""
New registration received:

Name: {registration.name}
Email: {registration.email}
Phone: {registration.country_code} {registration.phone_number}
Selected Events: {len(selected_events)} events
Registration Time: {registration.registration_date}

Selected Events:
{events_list}
"""

                owner_message_html = render_to_string('events/email/owner_notification.html', {
                    'name': registration.name,
                    'email': registration.email,
                    'phone': registration.phone_number,
                    'country_code': registration.country_code,
                    'registration': registration,
                    'selected_events': selected_events,
                })

                send_mail(
                    owner_subject,
                    owner_message_plain,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.OWNER_EMAIL],
                    fail_silently=False,
                    html_message=owner_message_html
                )
                
                print(f"✅ Email sent to user: {registration.email}")
                print(f"✅ Notification sent to owner: {settings.OWNER_EMAIL}")
                print(f"✅ Selected events: {len(selected_events)} events")
                
            except Exception as e:
                print(f"❌ Email sending failed: {e}")
                # Continue to success page even if email fails
            
            return render(request, 'events/success.html', {
                'registration': registration,
                'selected_events': selected_events,
            })
        else:
            print("❌ Form errors:", form.errors)
            # If form is invalid, still show the registration page with errors
            return render(request, 'events/registration.html', {
                'form': form,
                'selected_events_data': selected_events_json
            })
    else:
        form = RegistrationForm()
    
    return render(request, 'events/registration.html', {'form': form})

def success_view(request):
    return render(request, 'events/success.html')