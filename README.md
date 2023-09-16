# CashFlowPro

An API service for handling spending and revenue statistics.
The API is thoroughly 👓 **tested** and features comprehensive 📒 **Swagger documentation**. Additionally, it includes a 
user-friendly ⚡ **admin interface** for efficient data management.
Please do not forget to create your **secret key** using [Djecrety](https://djecrety.ir/).

## Installing using GitHub (macOS)
- `git clone https://github.com/IvanKorshunovE/CashFlowPro`
- `cd CashFlowPro`
- `python -m venv venv`
- `source venv/bin/activate`
- `pip install -r requirements.txt`
- `set SECRET_KEY=<your secret key, you may generate it using Djecrety>`

## API Endpoints
### Revenue Statistics: View and manage revenue statistics.

    /api/revenue/revenue-statistics/
Fetch a comprehensive list of revenue statistics, including aggregated data categorized by date and name. 
This data will also include related information about spending, encompassing details such as clicks, spending amounts, 
impressions, and conversions.

### Spend Statistics

    api/spending/spend-statistics/
Explore and oversee aggregated spending statistics categorized by date and name, encompassing spending details and 
associated revenue information.

### Swagger Documentation: 
    /api/schema/swagger-ui/
Access the Swagger documentation for the API.

### Redoc Documentation: 
    /api/schema/redoc/
Access the ReDoc documentation for the API.
