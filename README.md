# Rental_App
# Real Estate NL-to-SQL Demo

This repository demonstrates a **local, offline NL-to-SQL parser** for a sample real estate database.

## Features
## Database ERD

![Real Estate ERD](Rental_App/ERD_RentalApp.png)


- SQLite database with tables:
  - `users`, `properties`, `bookings`, `payments`, `reviews`, `property_photos`, `favorites`
- Sample data for tenants, landlords, properties and transactions
  
- Rule-based "LLM-like" NL-to-SQL parser
  
- Example queries:
  - Available apartments in a city under a rent threshold
  - Occupancy rate
  - Top 10 tenants by total rent paid
  - Average ratings of properties
  - Landlords generating most revenue

## Installation

```bash
git clone <repo_url>
cd realestate-nl2sql
pip install -r requirements.txt
