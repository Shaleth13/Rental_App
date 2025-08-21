import re
import sqlite3

def llm_like_nl_to_sql(nl_query):
    q = nl_query.lower()
    if any(x in q for x in ["available","bedroom","rent","apartment","house","villa","studio","london","bradford","manchester"]):
        sql = "SELECT * FROM properties WHERE 1=1"
        if "available" in q:
            sql += " AND status='available'"
        if "booked" in q:
            sql += " AND status='booked'"
        beds = re.findall(r"(\d+)\s*bed(room)?s?", q)
        if beds:
            sql += f" AND bedrooms>={beds[0][0]}"
        rents = re.findall(r"\$?(\d+[,|\d]*)", q)
        if rents:
            rent_val = int(rents[0].replace(",",""))
            sql += f" AND rent_price<{rent_val}"
        cities = ["bradford","london","manchester"]
        for city in cities:
            if city in q:
                sql += f" AND city='{city.title()}'"
        return sql

    if "occupancy rate" in q:
        return """
        SELECT 
            ROUND(CAST(COUNT(b.booking_id) AS FLOAT)/COUNT(p.property_id)*100,2) AS occupancy_rate
        FROM properties p
        LEFT JOIN bookings b
            ON p.property_id = b.property_id
            AND b.start_date >= date('now','-3 months')
            AND b.end_date <= date('now')
        WHERE p.city='Bradford'
        """

    if "top 10 tenants" in q or "total rent paid" in q:
        return """
        SELECT u.first_name || ' ' || u.last_name AS tenant_name, SUM(p.amount) AS total_paid
        FROM payments p
        JOIN users u ON p.tenant_id = u.user_id
        GROUP BY u.user_id
        ORDER BY total_paid DESC
        LIMIT 10
        """

    if "average rating" in q:
        return """
        SELECT prop.property_type, ROUND(AVG(r.rating),2) AS avg_rating
        FROM properties prop
        JOIN reviews r ON prop.property_id = r.property_id
        WHERE prop.property_type IN ('apartment','house')
        GROUP BY prop.property_type
        """

    if "most revenue" in q or "landlords generated" in q:
        return """
        SELECT u.first_name || ' ' || u.last_name AS landlord_name, SUM(pay.amount) AS total_revenue
        FROM properties prop
        JOIN users u ON prop.landlord_id = u.user_id
        JOIN bookings b ON b.property_id = prop.property_id
        JOIN payments pay ON pay.booking_id = b.booking_id
        WHERE strftime('%Y', pay.payment_date) = strftime('%Y','now')
        GROUP BY u.user_id
        ORDER BY total_revenue DESC
        """

    return "SELECT 'Query not recognized'"
