from datetime import date




currentMonth = date.today().month
currentYear = date.today().year

firstDateCurrentYear = date(date.today().year, 1, 1)
lastDateCurrentYear = date(date.today().year, 12, 31)

months = {1:"Gen", 2:"Feb", 3:"Mar", 4:"Abr", 5:"Mai", 6:"Jun", 7:"Jul", 8:"Ago", 9:"Set", 10:"Oct", 11:"Nov", 12:"Des"}