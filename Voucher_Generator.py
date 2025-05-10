from faker import Faker
import random
from datetime import timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

fake = Faker()

def calculate_final_settlement(join_date, last_day):
    total_days = (last_day - join_date).days
    absent_days = random.randint(0, min(15, total_days // 30))
    working_days = total_days - absent_days
    per_day_salary = random.randint(1500, 3000)

    amount_for_working_days = working_days * per_day_salary
    deduction_for_absent = absent_days * per_day_salary
    gratuity_fund = round(0.10 * amount_for_working_days, 2)
    provident_fund = round(0.12 * amount_for_working_days, 2)
    encashment_leaves = round(random.uniform(5000, 20000), 2)

    total_settlement = (
        amount_for_working_days
        - deduction_for_absent
        + gratuity_fund
        + provident_fund
        + encashment_leaves
    )

    return {
        "Total Working Days": total_days,
        "Working Days": working_days,
        "Absent Days": absent_days,
        "Per Day Salary": per_day_salary,
        "Amount for Working Days": amount_for_working_days,
        "Deduction for Absences": deduction_for_absent,
        "Gratuity Fund": gratuity_fund,
        "Provident Fund": provident_fund,
        "Encashment Leaves": encashment_leaves,
        "Total Final Settlement": round(total_settlement, 2)
    }

def generate_voucher():
    name = fake.name()
    designation = fake.job()
    department = fake.word().capitalize() + " Department"
    doj = fake.date_between(start_date='-10y', end_date='-2y')
    emp_number = fake.random_int(min=1000, max=9999)
    resignation_date = fake.date_between(start_date=doj, end_date='today')
    last_working_day = resignation_date + timedelta(days=random.randint(7, 30))
    
    settlement = calculate_final_settlement(doj, last_working_day)

    return {
        "Name": name,
        "Designation": designation,
        "Department": department,
        "Employee Number": emp_number,
        "Date of Joining": doj.strftime('%Y-%m-%d'),
        "Resignation Date": resignation_date.strftime('%Y-%m-%d'),
        "Last Working Day": last_working_day.strftime('%Y-%m-%d'),
        **settlement
    }

def create_pdf(voucher, index):
    file_name = f"Payment_Voucher_{index}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4
    margin = inch / 2

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2, height - margin, "Payment Voucher")

    c.setFont("Helvetica", 12)
    y = height - margin - 40
    line_height = 18

    for key, value in voucher.items():
        c.drawString(margin, y, f"{key}: {value}")
        y -= line_height
        if y < margin:
            c.showPage()
            y = height - margin - 40
            c.setFont("Helvetica", 12)

    c.save()

# Generate and save 10 vouchers as PDFs
for i in range(1, 11):
    voucher = generate_voucher()
    create_pdf(voucher, i)

print("✅ 10 payment voucher PDFs created successfully.")
