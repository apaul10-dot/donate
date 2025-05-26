import streamlit as st
import pandas as pd
from datetime import datetime, date
import time

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
    .main-header {
        font-size: 3rem;
        color: #1f4e79;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #2c5282;
        text-align: center;
        margin-bottom: 3rem;
    }
    .donation-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .stats-card {
        background: #f7fafc;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #4299e1;
        margin: 1rem 0;
    }
    .success-message {
        background: #c6f6d5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #38a169;
        color: #22543d;
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
    
    # Donation Section
    st.header("💰 Make Your Impact")
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
            
            # Success message
            st.balloons()
            st.markdown(f"""
            <div class="success-message">
                <h3>🎉 Donation Successful!</h3>
                <p><strong>${donation_amount:,}</strong> donated to support global education equality</p>
                <p>Your exclusive gala ticket has been secured!</p>
            </div>
            """, unsafe_allow_html=True)
            
            time.sleep(2)
            st.rerun()
        
        elif submit_donation and donation_amount < 5000:
            st.error("❌ Minimum donation of $5,000 required to secure your gala ticket.")
    
    # Ticket Status
    if st.session_state.ticket_purchased:
        st.header("🎫 Your Gala Ticket")
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
    
    # Donation History
    if st.session_state.donation_history:
        st.header("📊 Your Impact History")
        
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
