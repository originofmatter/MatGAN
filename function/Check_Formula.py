from .charge_neutrality_fast import check_neutrality
from .electronegativity_check_fast import check_electronegativity


def check_formula(formula):
	count_neutrality, count_electronegativity, count_both = [], [], []
	for i, form in enumerate(formula):
		# print(i, form)
		check_neu = check_neutrality(form)
		check_elect = check_electronegativity(form)
		if check_neu:
			count_neutrality.append(form)
		if check_elect:
			count_electronegativity.append(form)
		if check_neu == True and check_elect == True:
			count_both.append(form)
	neutrality_valid_percent = len(count_neutrality)/len(formula)
	electronegativity_valid_percent = len(count_electronegativity)/len(formula)
	both_valid_percent = len(count_both)/len(formula)
	return neutrality_valid_percent, electronegativity_valid_percent, both_valid_percent