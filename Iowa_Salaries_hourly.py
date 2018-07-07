"""This script inspects employee salary data from the State of Iowa database
retrieved online from: 
    
https://catalog.data.gov/dataset/state-of-iowa-salary-book

The data includes more than 500,000 entries giving the gender, job title, 
department, city of residence, pay, and travel expenses for each employee from 
2007 to 2017, inclusive. The database does not give employee age or tenure in 
the current position or length of employment with the State. The goal of this 
project is to infer hourly pay for employees based on the available 
predictors, realizing there may still be substantial variation due to variables
not available in the data set. Annual salaries were not predicted since many
employees likely only received salary for part of each year."""

# Import necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read in data (this includes approximately 30% of the data from the original file due to Github file size limits)
df = pd.read_csv('State_of_Iowa_Salary_Book_Excerpt.csv')

# Insert new column with estimated hourly pay
def hourly_sal(cols):
    base_sal = cols[0]
    total_sal = cols[1]
    if pd.isnull(base_sal):
        return
    elif base_sal.lower() == 'terminated' or base_sal.lower() == 'terminated ' or base_sal == 'HR' or base_sal == 'YR' or base_sal == 'HR+H517753' or base_sal == '20.12HR' or base_sal == '262.99DA':
        return
    else:
        base_sal = base_sal.strip()
        import re
        base_sal = re.split(' |/|-', base_sal)
        #base_sal = base_sal.split()
        #base_sal = base_sal.split('/')
        base_sal[0] = base_sal[0].replace(',', '')
        base_sal[0] = base_sal[0].replace('$', '')
        if base_sal[-1] == 'BW':
           hourly_sal = float(base_sal[0]) / 40 / 2
           # Remove entries with erroneous data (hourly pay very high or very low)
           if hourly_sal < 3000 and hourly_sal > 5 and hourly_sal != total_sal:
               return hourly_sal
           else:
               return
        elif base_sal[-1] == 'HR':
           hourly_sal =  float(base_sal[0])
           # Remove entries with erroneous data (hourly pay very high or very low)
           if hourly_sal < 3000 and hourly_sal > 5 and hourly_sal != total_sal:
               return hourly_sal
           else:
               return
        elif base_sal[-1] == 'YR' or len(base_sal) == 1:
           hourly_sal = float(base_sal[0]) / 40 / 52
           # Remove entries with seemingly erroneous data (hourly pay very high or very low)
           if hourly_sal < 3000 and hourly_sal > 5 and hourly_sal != total_sal:
               return hourly_sal
           else:
               return
        else:
           return
df['Hourly_Pay'] = df[['Base Salary', 'Total Salary Paid']].apply(hourly_sal, axis=1)

# POSITION TAGS
# Insert column to check if employee is head coach
def isheadcoach(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif position.lower() == 'head coach':
        return 1
    else:
        return 0
df['Head Coach'] = df[['Position']].apply(isheadcoach, axis = 1)

# Insert column to check if employee is coach
def iscoach(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'coach' in position.lower().split():
        return 1
    else:
        return 0
df['Coach'] = df[['Position']].apply(iscoach, axis = 1)

# Insert column to check if employee has "President" in title
def ispres(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'president' in position.lower().split():
        return 1
    else:
        return 0
df['Pres'] = df[['Position']].apply(ispres, axis = 1)

# Insert column to check if employee has "Vice" in title
def isvice(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('vice' in position.lower().split()) or ('vp' in position.lower().split()):
        return 1
    else:
        return 0
df['Vice'] = df[['Position']].apply(isvice, axis = 1)

# Insert column to check if employee has "Dean" in title
def isdean(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'dean' in position.lower().split():
        return 1
    else:
        return 0
df['Dean'] = df[['Position']].apply(isdean, axis = 1)

# Insert column to check if employee is physician
def isphysician(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'physician' in position.lower().split():
        return 1
    else:
        return 0
df['Physician'] = df[['Position']].apply(isphysician, axis = 1)

# Insert column to check if employee is attorney
def isattorney(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'attorney' in position.lower().split():
        return 1
    else:
        return 0
df['Attorney'] = df[['Position']].apply(isattorney, axis = 1)

# Insert column to check if employee is engineer
def iseng(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('engineer' in position.lower().split()) or ('eng' in position.lower().split()):
        return 1
    else:
        return 0
df['Eng'] = df[['Position']].apply(iseng, axis = 1)

# Insert column to check if employee is executive
def isexec(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('exec' in position.lower().split()) or ('executive' in position.lower().split()):
        return 1
    else:
        return 0
df['Exec'] = df[['Position']].apply(isexec, axis = 1)

# Insert column to check if employee works for lottery
def islottery(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'lottery' in position.lower().split():
        return 1
    else:
        return 0
df['Lott'] = df[['Position']].apply(islottery, axis = 1)

# Insert column to check if employee is graudate student
def isgrad(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('grad' in position.lower().split()) or (position.lower() == 'scholar/trainee'):
        return 1
    else:
        return 0
df['Grad'] = df[['Position']].apply(isgrad, axis = 1)

# Insert column to check if employee is graudate professor
def isprof(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('prof' in position.lower().split()) or ('professor' in position.lower().split()):
        return 1
    else:
        return 0
df['Prof'] = df[['Position']].apply(isprof, axis = 1)

# Insert column to check if employee is storekeeper
def isstore(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'storekeeper' in position.lower().split():
        return 1
    else:
        return 0
df['Store'] = df[['Position']].apply(isstore, axis = 1)

# Insert column to check if "Chief" appears in employee title
def ischief(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'chief' in position.lower().split():
        return 1
    else:
        return 0
df['Chief'] = df[['Position']].apply(ischief, axis = 1)

# Insert column to check if employee is a director
def isdir(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('director' in position.lower().split()) or ('dir' in position.lower().split()):
        return 1
    else:
        return 0
df['Dir'] = df[['Position']].apply(isdir, axis = 1)

# Insert column to check if employee is a secretary
def issec(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'secretary' in position.lower().split():
        return 1
    else:
        return 0
df['Sec'] = df[['Position']].apply(issec, axis = 1)

# Insert column to check if employee is an admin
def isadmin(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('admin' in position.lower().split()) or ('administrative' in position.lower().split()):
        return 1
    else:
        return 0
df['Admin'] = df[['Position']].apply(isadmin, axis = 1)

# Insert column to check if employee is a custodian
def iscust(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'custodian' in position.lower().split():
        return 1
    else:
        return 0
df['Cust'] = df[['Position']].apply(iscust, axis = 1)

# Insert column to check if employee is an intern
def isintern(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'intern' in position.lower().split():
        return 1
    else:
        return 0
df['Intern'] = df[['Position']].apply(isintern, axis = 1)

# Insert column to check if employee is in tech
def istech(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('tech' in position.lower().split()) or ('technology' in position.lower().split()):
        return 1
    else:
        return 0
df['Tech'] = df[['Position']].apply(istech, axis = 1)

# Insert column to check if employee is a teacher
def isteach(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('teacher' in position.lower().split()) or ('instructor' in position.lower().split()):
        return 1
    else:
        return 0
df['Teach'] = df[['Position']].apply(isteach, axis = 1)

# Insert column to check if employee's position is listed as 'Americorp'
def isamericorp(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'americorp' in position.lower().split():
        return 1
    else:
        return 0
df['Americorp'] = df[['Position']].apply(isamericorp, axis = 1)

# Insert column to check if employee's position is a correctional officer
def iscor(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'correctional' in position.lower().split():
        return 1
    else:
        return 0
df['Corr'] = df[['Position']].apply(iscor, axis = 1)

# Insert column to check if employee's position is a maintenance worker
def ismaint(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'maint' in position.lower().split():
        return 1
    else:
        return 0
df['Maint'] = df[['Position']].apply(ismaint, axis = 1)

# Insert column to check if employee's position is as clerk
def isclerk(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'clerk' in position.lower().split():
        return 1
    else:
        return 0
df['Clerk'] = df[['Position']].apply(isclerk, axis = 1)

# Insert column to check if employee's position is as sergeant
def isser(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'sergeant' in position.lower().split():
        return 1
    else:
        return 0
df['Serg'] = df[['Position']].apply(isser, axis = 1)

# Insert column to check if employee's position includes word 'network'
def isnet(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif 'network' in position.lower().split():
        return 1
    else:
        return 0
df['Net'] = df[['Position']].apply(isnet, axis = 1)

# Insert column to check if employee's position includes the word "athletics"
def isath(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('athletics' in position.lower().split()) or ('athletic' in position.lower().split()):
        return 1
    else:
        return 0
df['Ath'] = df[['Position']].apply(isath, axis = 1)

# Insert column to check if employee's position includes the word "aide"
def isaide(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('aide' in position.lower().split()):
        return 1
    else:
        return 0
df['Aide'] = df[['Position']].apply(isaide, axis = 1)

# Insert column to check if employee's position includes word "associate"
def isassoc(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('assoc' in position.lower().split()) or ('associate' in position.lower().split()):
        return 1
    else:
        return 0
df['Assoc'] = df[['Position']].apply(isassoc, axis = 1)

# Insert column to check if employee's position includes word "assistant"
def isassist(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('asst' in position.lower().split()) or ('assist' in position.lower().split()) or ('assistant' in position.lower().split()):
        return 1
    else:
        return 0
df['Assist'] = df[['Position']].apply(isassist, axis = 1)

# Insert column to check if employee's position includes word "adjunct"
def isadj(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('adjunct' in position.lower().split()) or ('adj' in position.lower().split()):
        return 1
    else:
        return 0
df['Adjunct'] = df[['Position']].apply(isadj, axis = 1)

# Insert column to check if employee's position includes word "monthly"
def ismonthly(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('monthly' in position.lower().split()):
        return 1
    else:
        return 0
df['Monthly'] = df[['Position']].apply(ismonthly, axis = 1)

# Insert column to check if employee's position includes number "1"
def isone(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('1' in position.lower().split()) or ('i' in position.lower().split()):
        return 1
    else:
        return 0
df['One'] = df[['Position']].apply(isone, axis = 1)

# Insert column to check if employee's position includes number "2"
def istwo(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('2' in position.lower().split()) or ('ii' in position.lower().split()):
        return 1
    else:
        return 0
df['Two'] = df[['Position']].apply(istwo, axis = 1)

# Insert column to check if employee's position includes number "3"
def isthree(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('3' in position.lower().split()) or ('iii' in position.lower().split()):
        return 1
    else:
        return 0
df['Three'] = df[['Position']].apply(isthree, axis = 1)

def isfour(cols):
    position = cols[0]
    if pd.isnull(position):
        return 0
    elif ('4' in position.lower().split()) or ('iv' in position.lower().split()):
        return 1
    else:
        return 0
df['Four'] = df[['Position']].apply(isfour, axis = 1)

# DEPARTMENT VALUES
# Insert column to check if employee's department is University of Iowa
def isuofi(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'University of Iowa':
        return 1
    else:
        return 0
df['U_of_I'] = df[['Department']].apply(isuofi, axis = 1)

# Insert column to check if employee's department is Iowa State University
def isistate(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Iowa State University':
        return 1
    else:
        return 0
df['Iowa_State'] = df[['Department']].apply(isistate, axis = 1)

# Insert column to check if employee's department is Department of Transportation
def isdot(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Transportation, Department of':
        return 1
    else:
        return 0
df['DOT'] = df[['Department']].apply(isdot, axis = 1)

# Insert column to check if employee's department is Department of Corrections
def isdoc(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Corrections, Department of':
        return 1
    else:
        return 0
df['DOC'] = df[['Department']].apply(isdoc, axis = 1)

# Insert column to check if employee's department is University of Northern Iowa
def isuni(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'University of Northern Iowa':
        return 1
    else:
        return 0
df['UNI'] = df[['Department']].apply(isuni, axis = 1)

# Insert column to check if employee's department is Judicial Branch
def isjb(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Judicial Branch':
        return 1
    else:
        return 0
df['JB'] = df[['Department']].apply(isjb, axis = 1)

# Insert column to check if employee's department is Dept. of Natural Resources
def isdnr(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Natural Resources, Department of':
        return 1
    else:
        return 0
df['DNR'] = df[['Department']].apply(isdnr, axis = 1)

# Insert column to check if employee's department is Dept. of Public Safety
def isdps(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Public Safety, Department of':
        return 1
    else:
        return 0
df['DPS'] = df[['Department']].apply(isdps, axis = 1)

# Insert column to check if employee's department is Iowa Veterans Home
def isivh(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Iowa Veterans Home':
        return 1
    else:
        return 0
df['IVH'] = df[['Department']].apply(isivh, axis = 1)

# Insert column to check if employee's department is Iowa Workforce Development
def isiwd(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Iowa Workforce Development':
        return 1
    else:
        return 0
df['IWD'] = df[['Department']].apply(isiwd, axis = 1)

# Insert column to check if employee's department is Department of Education
def isdoe(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Education, Department of':
        return 1
    else:
        return 0
df['DOE'] = df[['Department']].apply(isdoe, axis = 1)

# Insert column to check if employee's department is Dept. of Inspections and Appeals
def isdia(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Inspections & Appeals, Department of':
        return 1
    else:
        return 0
df['DIA'] = df[['Department']].apply(isdia, axis = 1)

# Insert column to check if employee's department is Dept. of Inspections and Appeals
def isleg(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Legislative Branch':
        return 1
    else:
        return 0
df['Leg'] = df[['Department']].apply(isleg, axis = 1)

# Insert column to check if employee's department is Dept. of Public Defense
def isdpd(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Public Defense, Department of':
        return 1
    else:
        return 0
df['DPD'] = df[['Department']].apply(isdpd, axis = 1)

# Insert column to check if employee's department is Dept. of Commerce
def isdcom(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Commerce, Department of':
        return 1
    else:
        return 0
df['DCom'] = df[['Department']].apply(isdcom, axis = 1)

# Insert column to check if employee's department is Dept. of Administrative Services
def isdas(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Administrative Services, Department of':
        return 1
    else:
        return 0
df['DAS'] = df[['Department']].apply(isdas, axis = 1)

# Insert column to check if employee's department is Board of Regents
def isbor(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Regents, Board of':
        return 1
    else:
        return 0
df['BoR'] = df[['Department']].apply(isbor, axis = 1)

# Insert column to check if employee's department is Attorney General
def isag(cols):
    dept = cols[0]
    if pd.isnull(dept):
        return 0
    elif dept == 'Attorney General, Office of':
        return 1
    else:
        return 0
df['AG'] = df[['Department']].apply(isag, axis = 1)

# TRAVEL AND SUBISTENCE INFORMATION
# Change Travel & Subsistence to zero if no value given
def trav(cols):
    trav_cost = cols[0]
    if pd.isnull(trav_cost):
        return 0
    else:
        return trav_cost
df['Travel & Subsistence'] = df[['Travel & Subsistence']].apply(trav, axis = 1)

# Drop entries with no salary data
df_an = df[df['Hourly_Pay'] > 0]

# Import data test categorical columns - gender
def gender_fil(cols):
    gen = cols[0]
    if gen in ['M', 'F']:
        return True
    else:
        return False
gender_fil = df_an[['Gender']].apply(gender_fil, axis = 1)
df_an = df_an[gender_fil]
gender = pd.get_dummies(df_an['Gender'], drop_first = True)
df_an.drop(['Gender'], axis=1, inplace=True)
df_an = pd.concat([df_an, gender], axis=1)


# PLOT SOME OF THE DATA
# 
# Create boxplot showing hourly pay by year
print('\nSALARY V. FISCAL YEAR:')
fig = plt.figure(figsize=(20, 6))
ax = plt.subplot(1, 11, 1)

ax.boxplot((df_an[df_an['Fiscal Year'] == 2007]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yticks(np.arange(0, 4))
ax.set_yticklabels(10.0**np.arange(0, 4))
ax.set_ylim(1, 3000)
ax.set_yscale('log')
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('2007')

ax = plt.subplot(1, 11, 2)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2008]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2008')

ax = plt.subplot(1, 11, 3)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2009]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2009')

ax = plt.subplot(1, 11, 4)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2010]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2010')

ax = plt.subplot(1, 11, 5)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2011]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2011')

ax = plt.subplot(1, 11, 6)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2012]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2012')

ax = plt.subplot(1, 11, 7)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2013]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2013')

ax = plt.subplot(1, 11, 8)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2014]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2014')

ax = plt.subplot(1, 11, 9)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2015]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2015')

ax = plt.subplot(1, 11, 10)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2016]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2016')

ax = plt.subplot(1, 11, 11)
ax.boxplot((df_an[df_an['Fiscal Year'] == 2017]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_title('2017')
plt.show()


# Create boxplot showing hourly pay by Gender
print('\nHOURLY PAY V. GENDER:')
fig = plt.figure(figsize=(9, 6))
ax = plt.subplot(1, 2, 1)

ax.boxplot((df_an[df_an['M'] == 1]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yticks(np.arange(0, 4))
ax.set_yticklabels(10.0**np.arange(0, 4))
ax.set_ylim(1, 3000)
ax.set_yscale('log')
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('Male')

ax = plt.subplot(1, 2, 2)
ax.boxplot((df_an[df_an['M'] == 0]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('Female')
plt.show()

# Create boxplot showing hourly pay by Head Coach Flag
print('\nHOURLY PAY V. "HEAD COACH" JOB FLAG:')
fig = plt.figure(figsize=(9, 6))
ax = plt.subplot(1, 2, 1)

ax.boxplot((df_an[df_an['Head Coach'] == 1]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yticks(np.arange(0, 4))
ax.set_yticklabels(10.0**np.arange(0, 4))
ax.set_ylim(1, 3000)
ax.set_yscale('log')
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('"Head Coach" in job title')

ax = plt.subplot(1, 2, 2)
ax.boxplot((df_an[df_an['Head Coach'] == 0]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('"Head Coach" not in job title')
plt.show()

# Create boxplot showing hourly pay by President Flag
print('\nHOURLY PAY V. "PRESIDENT" JOB FLAG:')
fig = plt.figure(figsize=(9, 6))
ax = plt.subplot(1, 2, 1)

ax.boxplot((df_an[df_an['Pres'] == 1]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yticks(np.arange(0, 4))
ax.set_yticklabels(10.0**np.arange(0, 4))
ax.set_ylim(1, 3000)
ax.set_yscale('log')
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('"President" in job title')

ax = plt.subplot(1, 2, 2)
ax.boxplot((df_an[df_an['Pres'] == 0]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('"President" not in job title')
plt.show()

# Create boxplot showing hourly pay by Chief Flag
print('\nHOURLY PAY V. "CHIEF" JOB FLAG:')
fig = plt.figure(figsize=(9, 6))
ax = plt.subplot(1, 2, 1)

ax.boxplot((df_an[df_an['Chief'] == 1]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yticks(np.arange(0, 4))
ax.set_yticklabels(10.0**np.arange(0, 4))
ax.set_ylim(1, 3000)
ax.set_yscale('log')
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('"Chief" in job title')

ax = plt.subplot(1, 2, 2)
ax.boxplot((df_an[df_an['Chief'] == 0]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('"Chief" not in job title')
plt.show()

# Create boxplot showing hourly pay by Attorney Flag
print('\nHOURLY PAY V. "ATTORNEY" JOB FLAG:')
fig = plt.figure(figsize=(9, 6))
ax = plt.subplot(1, 2, 1)

ax.boxplot((df_an[df_an['Attorney'] == 1]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yticks(np.arange(0, 4))
ax.set_yticklabels(10.0**np.arange(0, 4))
ax.set_ylim(1, 3000)
ax.set_yscale('log')
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('"Attorney" in job title')

ax = plt.subplot(1, 2, 2)
ax.boxplot((df_an[df_an['Attorney'] == 0]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('"Attorney" not in job title')
plt.show()

# Create boxplot showing hourly pay by Legislative Branch Flag
print('\nHOURLY PAY V. "LEGISLATIVE BRANCH" DEPARTMENT FLAG:')
fig = plt.figure(figsize=(9, 6))
ax = plt.subplot(1, 2, 1)

ax.boxplot((df_an[df_an['Leg'] == 1]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yticks(np.arange(0, 4))
ax.set_yticklabels(10.0**np.arange(0, 4))
ax.set_ylim(1, 3000)
ax.set_yscale('log')
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('Legislative Branch Employee')

ax = plt.subplot(1, 2, 2)
ax.boxplot((df_an[df_an['U_of_I'] == 0]['Hourly_Pay']), notch = True, whis = [5, 95], patch_artist = True)
ax.set_yscale('log')
ax.set_ylim(1, 3000)
ax.set_ylabel('Hourly Pay [$]')
ax.set_title('Not Legislative Branch Employee')
plt.show()

# Create training and test sets
from sklearn.model_selection import train_test_split
y = df_an['Hourly_Pay']
# Drop columns not used in the analysis
X = df_an.drop(['Agency/Institution', 'Base Salary', 'Position', 'Base Salary Date', 'Total Salary Paid', 'Name', 'Place of Residence', 'Hourly_Pay', 'Department', 'Travel & Subsistence', 'Fiscal Year'], axis = 1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30)

# LINEAR REGRESSION
# Create the Linear Regression Training Model using all predictors
from sklearn.linear_model import LinearRegression
lm = LinearRegression()
lm.fit(X_train,y_train)

def truncate(f, n):
    '''Function truncates float'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

# Create predictions and plot outcome
pred = lm.predict(X_test)
from decimal import Decimal
error_1 = ((np.array(y_test) - pred)**2).sum()
print('\n\nLINEAR REGRESSION RESULTS')
print('------------------------------------------------------------------')
print('\nPredictors with large p values were removed from the analysis using backward elimination.')
print('\nFor linear regression using all estimators, the root mean squared error is :', ('%.2E' % Decimal(error_1)), '.\n')

# Calculate mean error
abs_error = np.absolute(np.array(y_test) - pred)
abs_err_mean = abs_error.mean()
abs_err_median = np.median(abs_error)

abs_err_mean_pct = (abs_error/np.array(y_test)).mean()*100
abs_err_median_pct = np.median((abs_error/np.array(y_test)))*100

print('The mean hourly pay error of this model is $', truncate(abs_err_mean,2), ' while the median pay error is $', truncate(abs_err_median,2), '.\n\n')
print('This represents a mean hourly pay error of ', truncate(abs_err_mean/y_test.mean()*100,1),'% and a median pay error of ', truncate(abs_err_median_pct,1),'%')

# Check Linear Regression Statistics
import statsmodels.formula.api as sm
X_opt = X
regressor_OLS = sm.OLS(endog = y, exog = X_opt).fit()
print('Statistical Summary: \n', regressor_OLS.summary(), '\n\n')

# Plot Actual Salary v Predicted Salary - Linear Regression
print('\nLINEAR REGRESSION RESULTS PLOT - Actual Hourly Pay v Predicted Pay')
plt.figure(figsize = (6,6))
plt.scatter(y_test, pred)
plt.plot(range(0,500), ls = '--', c = 'k')
plt.xlabel('Actual Hourly Pay [$]')
plt.ylabel('Predicted Hourly Pay [$]')
plt.xlim(1, 500)
plt.ylim(1, 500)
plt.title('Linear Regression Results')
plt.show()
plt.clf()
ax.clear()

# RANDOM FOREST REGRESSION
# Fitting SVR to the dataset
from sklearn.ensemble import RandomForestRegressor
rfr = RandomForestRegressor(n_estimators = 100)
rfr.fit(X_train, y_train)

# Create predictions and plot outcome of Random Forest model
pred_rfr = rfr.predict(X_test)
error_rfr = ((np.array(y_test) - pred_rfr)**2).sum()
print('\n\nRANDOM FOREST REGRESSION RESULTS')
print('------------------------------------------------------------------')
print('\nFor Random Forest Regression, the root mean squared error is :', ('%.2E' % Decimal(error_rfr)), '.\n')

# Calculate mean error
abs_error_rfr = np.absolute(np.array(y_test) - pred_rfr)
abs_err_rfr_mean = abs_error_rfr.mean()
abs_err_rfr_median = np.median(abs_error_rfr)

abs_err_rfr_mean_pct = (abs_error_rfr/np.array(y_test)).mean()*100
abs_err_rfr_median_pct = np.median((abs_error_rfr/np.array(y_test)))*100


print('The mean hourly pay error of this model is $', truncate(abs_err_rfr_mean,2), ' while the median pay error is $', truncate(abs_err_rfr_median,2), '.\n\n')
print('This represents a mean hourly pay error of ', truncate(abs_err_rfr_mean/y_test.mean()*100,1),'% and a median pay error of ', truncate(abs_err_rfr_median_pct,1),'%')
# Plot Actual Salary v Predicted Salary - Random Forest Regression
print('\nRANDOM FOREST REGRESSION RESULTS PLOT - Actual Hourly Pay v Predicted Pay')
plt.figure(figsize = (6,6))
plt.scatter(y_test, pred_rfr)
plt.plot(range(0,500), ls = '--', c = 'k')
plt.xlabel('Actual Hourly Pay [$]')
plt.ylabel('Predicted Hourly Pay [$]')
plt.xlim(1, 500)
plt.ylim(1, 500)
plt.title('Random Forest Regression Results')
plt.show()
plt.clf()
ax.clear()
