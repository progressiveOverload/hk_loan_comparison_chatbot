import streamlit as st
import requests
from bs4 import BeautifulSoup

# Collect user input for amount and maturity amount
amount = st.number_input("Enter the loan amount", min_value=0)
maturity_amount = st.number_input("Enter the maturity amount", min_value=0)

if st.button("Compare Credits"):
    # Construct the URL with user parameters
    url = f"https://www.hangikredi.com/kredi/ihtiyac-kredisi/sorgulama?amount={amount}&maturity={maturity_amount}"
    
    # Make a GET request to the URL
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract the relevant data
        credits = []
        for credit in soup.select('.product-card.lazy6090'):  # Adjust the selector based on the actual HTML structure
            title = credit.select_one('.product-card__header span[data-testid="name"]').get_text(strip=True)
            description = credit.select_one('.product-card__title[data-testid="cardTitle"]').get_text(strip=True)
            image = credit.select_one('.product-card__header img')['src']
            interest_rate = credit.select_one('.product-card_rates em[data-testid="rate"]').get_text(strip=True)
            monthly_installment = credit.select_one('.product-card__monthly-installment .product-card_rates[data-testid="monthlyInstallment"]').get_text(strip=True)
            total_payment = credit.select_one('.product-card__total-payment .product-card_rates[data-testid="totalAmount"]').get_text(strip=True)
            
            credits.append({
                "title": title,
                "description": description,
                "image": image,
                "interest_rate": interest_rate,
                "monthly_installment": monthly_installment,
                "total_payment": total_payment
            })
        
        # Display the credits in Streamlit
        st.subheader("Compare Credits")
        for credit in credits:
            try:
                st.image(credit["image"], use_container_width=True)
            except Exception as e:
                st.image("https://via.placeholder.com/150", use_container_width=True)
            st.markdown(f"### {credit['title']}")
            st.markdown(f"**Interest Rate:** {credit['interest_rate']}")
            st.markdown(f"**Monthly Installment:** {credit['monthly_installment']}")
            st.markdown(f"**Total Payment:** {credit['total_payment']}")
            st.markdown("---")
    else:
        st.error("Failed to retrieve data. Please try again later.")