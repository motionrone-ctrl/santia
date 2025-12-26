# Santia - Teleconsultation Platform

## Original Problem Statement
Build a modern, trust-focused teleconsultation website for brand "Santia".
- Language: French
- Audience: Cameroon
- Currency: FCFA

### Branding
- Colors: #0A2540 (bleu nuit), #2ECC71 (vert santé), #FFFFFF
- Typography: Poppins Bold (headings), Inter Regular (body)
- Slogan: "Consultation médicale en ligne"

## Architecture & Features Implemented

### Backend (FastAPI)
- `/api/intake` - POST endpoint for form submission
- `/api/intakes` - GET endpoint to list all intake records
- MongoDB integration for data persistence
- Input validation with Pydantic models

### Frontend (React)
- **Pages:**
  - `/` - Home page with Hero, Specialties, How it works, Trust, FAQ, Footer
  - `/consultation` - Multi-step intake form (4 steps)
  - `/confirmation` - Thank you page after submission

- **Components:**
  - Navbar (responsive with mobile menu)
  - Hero section with CTA
  - Specialties grid (6 categories)
  - How it works (3 steps)
  - Trust section (6 trust badges)
  - FAQ with accordion
  - Footer with contact info

### Multi-step Form (Consultation Page)
1. **Step 1:** Category selection (Santé sexuelle, Addictions, Perte de poids, Sommeil, Cheveux, Fertilité)
2. **Step 2:** Symptoms description + duration + medical history
3. **Step 3:** Patient info (name, age, gender, phone, email, city)
4. **Step 4:** Recap + consent checkbox + submit

### Design Features
- Mobile-first responsive design
- Warm, accessible medical aesthetic
- Soft animations (fade-in-up, stagger effects)
- Interactive hover states
- Progress bar on form
- Urgence disclaimer visible on all pages

## Tech Stack
- **Frontend:** React, Tailwind CSS, Shadcn/UI, Lucide React icons
- **Backend:** FastAPI, Motor (async MongoDB driver), Pydantic
- **Database:** MongoDB

## Next Tasks / Enhancements
1. **Payment Integration:** Add Stripe/Mobile Money for consultation fees (5000 FCFA+)
2. **Email Notifications:** Send confirmation email to patient after submission
3. **Admin Dashboard:** Create admin panel to manage and respond to intake requests
4. **Doctor Assignment:** Automatic assignment to available doctors
5. **SMS Notifications:** Twilio integration for SMS alerts
6. **Real-time Chat:** Add WebSocket chat between patient and doctor
7. **Appointment Scheduling:** Calendar integration for booking specific time slots
