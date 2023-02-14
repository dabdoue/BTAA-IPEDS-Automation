import click_functions
def get_data(year, driver):
    # regions and whether land grant
    click_functions.click_dropdown("Institutional Characteristics", driver)
    if year < 2019: # special case with years older than 2019, where dropdown layout was slightly different
        click_functions.click_something('//div[@filetitle="Institutional Characteristics"]', driver)
    click_functions.click_dropdown("Directory information", driver)
    if year >= 2019:
        click_functions.click_dropdown("Institution classifications", driver)
    click_functions.click_checkbox("Bureau of Economic Analysis (BEA)", driver)
    click_functions.click_checkbox("Land Grant Institution", driver)
    # finding enrollment info
    print("cur year = " + str(year))
    if year < 2021:
        click_functions.click_dropdown("Fall Enrollment", driver)
        click_functions.click_dropdown("Frequently used enrollment variables", driver)
        # total enrollment
        click_functions.click_checkbox("Total  enrollment", driver) # not a typo - needs two spaces because typo on website
        # full-time enrollment
        click_functions.click_checkbox("Full-time enrollment", driver)
        # full-time undergrad
        click_functions.click_checkbox("Full-time undergraduate enrollment", driver)
        # full time grad
        click_functions.click_checkbox("Full-time graduate enrollment", driver)
    else:
        click_functions.click_dropdown("12-Month Enrollment", driver)
        click_functions.click_dropdown("12-month unduplicated headcount by race/ethnicity, gender and level of student: 2020-21", driver)
        click_functions.click_checkbox("Grand total", driver)
        click_functions.click_dropdown("12-month instructional activity: 2020-21", driver)
        click_functions.click_checkbox("Reported full-time equivalent (FTE) undergraduate enrollment, 2020-21", driver)
        click_functions.click_checkbox("Reported full-time equivalent (FTE) graduate enrollment, 2020-21", driver)
    # Num Awarded PhD degrees
    click_functions.click_dropdown("Completions", driver)
    click_functions.click_dropdown("Total awards/degrees", driver)
    click_functions.click_checkbox("research/scholarship", driver)
    # finding public research expenses
    click_functions.click_dropdown("Finance", driver)
    click_functions.click_dropdown("Public institutions - GASB", driver)
    click_functions.click_dropdown("Expenses and other deductions", driver)
    click_functions.click_checkbox("Research - Current year total", driver)
    # finding private research expenses
    click_functions.click_dropdown("Private not-for-profit institutions or Public institutions using FASB", driver)
    click_functions.click_dropdown("Expenses by functional and natural classification", driver)
    click_functions.click_checkbox("Research-Total amount", driver)
    # finding staff numbers
    click_functions.click_dropdown("Fall Staff", driver)
    click_functions.click_dropdown("Full-time equivalent staff", driver)
    if year >= 2013:
        click_functions.click_checkbox("Instructional, research and public service FTE", driver)
        click_functions.click_checkbox("Instructional FTE", driver)
    else:
        click_functions.click_checkbox("Postsecondary Teachers FTE staff", driver)
        click_functions.click_checkbox("Postsecondary Teachers Instructional FTE", driver)
