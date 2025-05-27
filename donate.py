import streamlit as st
import pandas as pd
from datetime import datetime, date
import time
from io import BytesIO
from fpdf import FPDF

# Page configuration
st.set_page_config(
    page_title="Global Education Inequality Ball",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    html, body, .stApp {
        font-family: 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif !important;
        background: linear-gradient(135deg, #101418 0%, #181c20 100%) !important;
        color: #f8fff8 !important;
    }
    .block-container {
        max-width: 900px !important;
        margin: 0 auto !important;
        padding: 2.5rem 2rem 2.5rem 2rem !important;
        background: #181c20 !important;
        border-radius: 18px !important;
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.25);
    }
    .main-header {
        font-size: 3.2rem;
        color: #eaffd0;
        text-align: center;
        margin-bottom: 2.2rem;
        font-weight: 800;
        text-shadow: 0 2px 12px #081c15;
        letter-spacing: 1.5px;
        padding-top: 0.5rem;
    }
    .subtitle {
        font-size: 1.35rem;
        color: #b7e4c7;
        text-align: center;
        margin-bottom: 2.5rem;
        font-weight: 500;
    }
    .section-divider {
        border: none;
        border-top: 2px solid #40916c;
        margin: 2.5rem 0 2rem 0;
    }
    .donation-card, .stats-card, .success-message {
        background: #23272b !important;
        color: #f8fff8 !important;
        border-radius: 16px;
        box-shadow: 0 4px 24px 0 rgba(0,0,0,0.18);
        margin: 1.5rem 0;
        padding: 2rem 2rem 1.5rem 2rem;
        transition: box-shadow 0.2s;
    }
    .donation-card:hover, .stats-card:hover {
        box-shadow: 0 8px 32px 0 rgba(0,0,0,0.28);
    }
    .stats-card {
        background: #181c20 !important;
        border-left: 6px solid #40916c;
        padding: 1.5rem 2rem;
        margin: 1.2rem 0;
    }
    .success-message {
        background: #183a1d !important;
        border-left: 6px solid #38b000;
        color: #eaffd0 !important;
        font-weight: 600;
    }
    .stButton>button {
        background: linear-gradient(90deg, #204529 0%, #40916c 100%) !important;
        color: #f8fff8 !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.15rem !important;
        padding: 0.8rem 2rem !important;
        box-shadow: 0 2px 8px 0 rgba(0,0,0,0.18);
        margin-top: 0.7rem;
        transition: background 0.2s, color 0.2s, box-shadow 0.2s;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #38b000 0%, #081c15 100%) !important;
        color: #eaffd0 !important;
        box-shadow: 0 4px 16px 0 rgba(0,0,0,0.28);
    }
    .stTextInput>div>input, .stTextInput>div>textarea {
        background: #23272b !important;
        color: #eaffd0 !important;
        border-radius: 10px !important;
        border: 2px solid #40916c !important;
        font-size: 1.05rem !important;
        padding: 0.6rem 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    .stDataFrame, .stDataFrame table {
        background: #181c20 !important;
        color: #eaffd0 !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
    }
    .stMetric {
        background: #23272b !important;
        color: #eaffd0 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        margin-bottom: 1rem !important;
    }
    .stSelectbox>div>div, .stMultiSelect>div>div {
        background: #23272b !important;
        color: #eaffd0 !important;
        border-radius: 10px !important;
        font-size: 1.05rem !important;
    }
    .stNumberInput>div>input {
        background: #23272b !important;
        color: #eaffd0 !important;
        border-radius: 10px !important;
        border: 2px solid #40916c !important;
        font-size: 1.05rem !important;
    }
    .stSidebar {
        background: #181c20 !important;
        color: #eaffd0 !important;
        border-right: 2px solid #40916c;
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        border-radius: 0 18px 18px 0 !important;
        box-shadow: 2px 0 16px 0 rgba(0,0,0,0.18);
    }
    .stExpanderHeader {
        background: #23272b !important;
        color: #eaffd0 !important;
        border-radius: 10px 10px 0 0 !important;
        font-weight: 600;
    }
    .stExpanderContent {
        background: #181c20 !important;
        color: #eaffd0 !important;
        border-radius: 0 0 10px 10px !important;
    }
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        background: #23272b;
    }
    ::-webkit-scrollbar-thumb {
        background: #40916c;
        border-radius: 4px;
    }
    /* Form tweaks */
    .stForm {
        margin-top: 1.5rem !important;
        margin-bottom: 1.5rem !important;
        padding: 1.5rem 1.5rem 1rem 1.5rem !important;
        background: #23272b !important;
        border-radius: 14px !important;
        box-shadow: 0 2px 12px 0 rgba(0,0,0,0.18);
    }
    /* Responsive tweaks */
    @media (max-width: 900px) {
        .block-container {
            padding: 1rem !important;
        }
        .main-header {
            font-size: 2.1rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'total_donations' not in st.session_state:
    st.session_state.total_donations = 0
if 'ticket_purchased' not in st.session_state:
    st.session_state.ticket_purchased = False
if 'donation_history' not in st.session_state:
    st.session_state.donation_history = []

# Global organizations data
organizations = {
    "Room to Read": {
        "region": "Global",
        "focus": "Girls' education and literacy",
        "description": "Working in 17 countries to transform millions of lives through education"
    },
    "Malala Fund": {
        "region": "Global",
        "focus": "Girls' education advocacy",
        "description": "Advocating for 12 years of free, safe, quality education for every girl"
    },
    "Teach for All": {
        "region": "Global",
        "focus": "Teacher training and leadership",
        "description": "Developing collective leadership to ensure all children can fulfill their potential"
    },
    "Save the Children": {
        "region": "Conflict Zones",
        "focus": "Emergency education",
        "description": "Providing education in emergencies and conflict-affected areas"
    },
    "World Vision Education": {
        "region": "Sub-Saharan Africa",
        "focus": "Community-based education",
        "description": "Building schools and training teachers in underserved communities"
    },
    "UNICEF Education": {
        "region": "Global",
        "focus": "Universal education access",
        "description": "Working to ensure every child has access to quality education"
    }
}

def main():
    # Header
    st.markdown('<h1 class="main-header">🎓 Global Education Inequality Ball</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">A Biannual Gala for Global Education Equality</p>', unsafe_allow_html=True)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=400", 
                caption="Education is a human right")
        
        if not st.session_state.logged_in:
            st.header("🔐 Login Required")
            st.write("You must log in and make a substantial donation to secure your ticket to this exclusive gala.")
        else:
            st.header(f"Welcome, {st.session_state.user_name}!")
            st.write(f"Total Donations: ${st.session_state.total_donations:,}")
            if st.session_state.ticket_purchased:
                st.success("✅ Ticket Secured!")
            else:
                st.warning("⚠️ Minimum $5,000 donation required for ticket")
    
    # Main content
    if not st.session_state.logged_in:
        login_section()
    else:
        main_dashboard()

def login_section():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.header("🚪 Member Login")
        st.write("Access to the Global Education Inequality Ball is exclusive to verified philanthropists and education advocates.")
        
        with st.form("login_form"):
            name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email Address", placeholder="your.email@domain.com")
            organization = st.text_input("Organization/Company", placeholder="Your organization")
            
            st.write("---")
            st.subheader("Philanthropic Background")
            previous_donations = st.selectbox(
                "Previous charitable donations (annual)",
                ["Under $1,000", "$1,000 - $10,000", "$10,000 - $50,000", 
                 "$50,000 - $100,000", "Over $100,000"]
            )
            
            education_interest = st.multiselect(
                "Areas of interest in education",
                ["Girls' Education", "Conflict Zone Education", "Teacher Training", 
                 "Educational Technology", "Adult Literacy", "Early Childhood Development"]
            )
            
            submit = st.form_submit_button("🔓 Request Access", use_container_width=True)
            
            if submit and name and email:
                st.session_state.logged_in = True
                st.session_state.user_name = name
                st.success("Welcome! You now have access to make donations and secure your ticket.")
                time.sleep(1)
                st.rerun()

def main_dashboard():
    # Event Information
    st.header("🌍 About the Global Education Inequality Ball")
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        **Next Event**: March 15, 2025 | New York City
        
        The Global Education Inequality Ball brings together influential leaders, philanthropists, 
        and advocates to address the crisis of education access affecting 250 million children worldwide.
        
        This exclusive biannual gala focuses on:
        - **Gender Equality**: Supporting the 122 million girls without access to education
        - **Conflict Zones**: Rebuilding education systems in war-torn regions
        - **Digital Divide**: Providing internet access and technology
        - **Teacher Training**: Supporting educators in underserved communities
        """)
    
    with col2:
        st.markdown("""
        <div class="stats-card">
            <h3>🎯 Impact Goals</h3>
            <ul>
                <li><strong>250M</strong> children out of school</li>
                <li><strong>122M</strong> girls denied education</li>
                <li><strong>$5B</strong> funding gap annually</li>
                <li><strong>17</strong> countries in crisis</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Top Donors Leaderboard (Sample Data)
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.subheader("🏆 Top Donors Leaderboard")
    leaderboard_data = [
        {"Name": "Ava Smith", "Amount": 50000},
        {"Name": "Liam Chen", "Amount": 35000},
        {"Name": "Noah Patel", "Amount": 25000},
        {"Name": "Sophia Lee", "Amount": 20000},
        {"Name": "You", "Amount": st.session_state.total_donations},
    ]
    leaderboard_df = pd.DataFrame(leaderboard_data).sort_values(by="Amount", ascending=False).reset_index(drop=True)
    st.markdown('<div class="donation-card">', unsafe_allow_html=True)
    st.table(leaderboard_df.style.format({"Amount": "$ {:,.0f}"}))
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Donation Section
    st.header("💰 Make Your Impact")
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.write("**Minimum donation of $5,000 required to secure your exclusive gala ticket.**")
    
    # Organization selection
    selected_orgs = st.multiselect(
        "Select organizations to support:",
        list(organizations.keys()),
        default=list(organizations.keys())[:3]
    )
    
    if selected_orgs:
        # Display selected organizations
        for org in selected_orgs:
            with st.expander(f"📚 {org} - {organizations[org]['region']}"):
                st.write(f"**Focus**: {organizations[org]['focus']}")
                st.write(organizations[org]['description'])
    
    # Donation form
    with st.form("donation_form"):
        st.subheader("💳 Donation Details")
        
        col1, col2 = st.columns(2)
        with col1:
            donation_amount = st.number_input(
                "Donation Amount ($)", 
                min_value=100, 
                max_value=1000000, 
                value=5000, 
                step=500
            )
        
        with col2:
            donation_frequency = st.selectbox(
                "Donation Type",
                ["One-time", "Monthly for 1 year", "Annual for 5 years"]
            )
        
        # Split donation across organizations
        if selected_orgs and len(selected_orgs) > 1:
            st.write("**Donation Distribution:**")
            split_amount = donation_amount / len(selected_orgs)
            for org in selected_orgs:
                st.write(f"• {org}: ${split_amount:,.2f}")
        
        # Payment details (simulated)
        st.subheader("💳 Payment Information")
        col1, col2 = st.columns(2)
        with col1:
            card_number = st.text_input("Card Number", placeholder="**** **** **** ****")
            card_name = st.text_input("Cardholder Name")
        with col2:
            expiry = st.text_input("MM/YY", placeholder="12/25")
            cvv = st.text_input("CVV", placeholder="123", type="password")
        
        submit_donation = st.form_submit_button("🎯 Complete Donation & Secure Ticket", use_container_width=True)
        
        if submit_donation and donation_amount >= 5000:
            # Process donation
            st.session_state.total_donations += donation_amount
            st.session_state.ticket_purchased = True
            
            # Add to donation history
            donation_record = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "amount": donation_amount,
                "organizations": selected_orgs,
                "frequency": donation_frequency
            }
            st.session_state.donation_history.append(donation_record)
            st.session_state.last_donation = donation_record
            
            # Success message
            st.balloons()
            st.markdown(f"""
            <div class="success-message">
                <h3>🎉 Donation Successful!</h3>
                <p><strong>${donation_amount:,}</strong> donated to support global education equality</p>
                <p>Your exclusive gala ticket has been secured!</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif submit_donation and donation_amount < 5000:
            st.error("❌ Minimum donation of $5,000 required to secure your gala ticket.")

    # Show PDF download button after form, if last_donation is set
    if 'last_donation' in st.session_state and st.session_state.last_donation:
        def generate_pdf_receipt(donation, user_name):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=16)
            pdf.cell(0, 12, "Donation Receipt", ln=True, align="C")
            pdf.set_font("Arial", size=12)
            pdf.ln(8)
            pdf.cell(0, 10, f"Date: {donation['date']}", ln=True)
            pdf.cell(0, 10, f"Donor: {user_name}", ln=True)
            pdf.cell(0, 10, f"Amount: ${donation['amount']:,}", ln=True)
            pdf.cell(0, 10, f"Organizations: {', '.join(donation['organizations'])}", ln=True)
            pdf.cell(0, 10, f"Donation Type: {donation['frequency']}", ln=True)
            pdf.ln(8)
            pdf.multi_cell(0, 10, "Thank you for your generous support of global education equality!\nThis receipt can be used for your records.")
            return pdf.output(dest='S').encode('latin1')
        pdf_bytes = generate_pdf_receipt(st.session_state.last_donation, st.session_state.user_name)
        if pdf_bytes:
            st.download_button(
                label="📄 Download Donation Receipt (PDF)",
                data=pdf_bytes,
                file_name=f"donation_receipt_{st.session_state.last_donation['date']}.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    
    # Ticket Status
    if st.session_state.ticket_purchased:
        st.header("🎫 Your Gala Ticket")
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        ticket_col1, ticket_col2 = st.columns([1, 1])
        
        with ticket_col1:
            st.markdown("""
            <div class="donation-card">
                <h3>🌟 VIP Gala Access Confirmed</h3>
                <p><strong>Event</strong>: Global Education Inequality Ball 2025</p>
                <p><strong>Date</strong>: March 15, 2025</p>
                <p><strong>Venue</strong>: The Plaza Hotel, New York</p>
                <p><strong>Dress Code</strong>: Black-tie with educational theme elements</p>
                <p><strong>Your Contribution</strong>: $""" + f"{st.session_state.total_donations:,}" + """</p>
            </div>
            """, unsafe_allow_html=True)
        
        with ticket_col2:
            st.subheader("🎭 Event Highlights")
            st.write("""
            - **Keynote**: Malala Yousafzai
            - **Performance**: Global Youth Orchestra
            - **Auction**: Rare books & educational experiences
            - **Awards**: Global Education Champions
            - **Networking**: 500+ philanthropists & leaders
            """)

        # RSVP & Table Selection
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        st.subheader("🍽️ RSVP & Table Selection")
        if 'rsvp_info' not in st.session_state:
            with st.form("rsvp_form"):
                meal = st.selectbox("Meal Preference", ["Vegetarian", "Vegan", "Chicken", "Fish", "Beef", "Gluten-Free"])
                table = st.number_input("Preferred Table Number (1-50)", min_value=1, max_value=50, value=1)
                special = st.text_area("Special Requests (optional)")
                submit_rsvp = st.form_submit_button("RSVP Now", use_container_width=True)
                if submit_rsvp:
                    st.session_state.rsvp_info = {
                        "meal": meal,
                        "table": table,
                        "special": special
                    }
                    st.success("Your RSVP has been received! We look forward to seeing you at the gala.")
        else:
            rsvp = st.session_state.rsvp_info
            st.markdown(f"""
            <div class="donation-card">
                <h4>✅ RSVP Confirmed</h4>
                <ul>
                    <li><strong>Meal:</strong> {rsvp['meal']}</li>
                    <li><strong>Table:</strong> {rsvp['table']}</li>
                    <li><strong>Special Requests:</strong> {rsvp['special'] if rsvp['special'] else 'None'}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Donation History
    if st.session_state.donation_history:
        st.header("📊 Your Impact History")
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
        
        # Create DataFrame for history
        df = pd.DataFrame(st.session_state.donation_history)
        df['organizations'] = df['organizations'].apply(lambda x: ', '.join(x))
        
        st.dataframe(
            df,
            column_config={
                "date": "Date",
                "amount": st.column_config.NumberColumn("Amount ($)", format="$%d"),
                "organizations": "Organizations Supported",
                "frequency": "Donation Type"
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Impact metrics
        total_impact = sum([d['amount'] for d in st.session_state.donation_history])
        st.metric("Total Impact", f"${total_impact:,}", f"+${total_impact:,} for global education")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌍 <strong>Global Education Inequality Ball</strong> | Together, we can ensure every child has access to quality education</p>
    <p>Contact: info@globaleducationball.org | +1 (555) 123-EDUCATION</p>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
