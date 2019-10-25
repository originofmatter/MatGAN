import time
import smact
from smact import neutral_ratios
import numpy as np
import pymatgen as mg

start_time = time.time()

def check_neutrality(formula):
    comp = mg.Composition(formula)
    reduce_formula = comp.get_el_amt_dict()
    element_num = len(list(reduce_formula.keys()))

    if element_num == 1:
        return True
    elif element_num == 2:
        return check_neutrality_2(formula)
    elif element_num == 3:
        return check_neutrality_3(formula)
    elif element_num == 4:
        return check_neutrality_4(formula)
    elif element_num == 5:
        return check_neutrality_5(formula)
    elif element_num == 6:
        return check_neutrality_6(formula)
    elif element_num == 7:
        return check_neutrality_7(formula)
    elif element_num == 8:
        return check_neutrality_8(formula)
    else:
        raise Exception('Not implemented: contact 897902311@qq.com')
        return False

def check_neutrality_2(formula):
    charge_neutral_count = 0
    comp = mg.Composition(formula)
    reduce_formula = comp.get_el_amt_dict()
    list_of_elements = list(reduce_formula.keys())
    stoichs = list(
                np.array(list(reduce_formula.values())).astype(np.int32)[:,np.newaxis]
            )
    max_num = max(reduce_formula.values())
    for i, ele_a in enumerate(list_of_elements):
        for ox_a in smact.Element(ele_a).oxidation_states:
            for j, ele_b in enumerate(list_of_elements[i+1:]):
                for ox_b in smact.Element(ele_b).oxidation_states:                    
                            
                    # Checks if the combination is charge neutral before printing it out! #                        
                    # neutral_ratios(oxidations, stoichs=False, threshold=5) #speed up by providing stoichs 
                    # cn_e, cn_r = neutral_ratios([ox_a, ox_b], threshold = int(max_num))
                    cn_e, cn_r = neutral_ratios([ox_a, ox_b], stoichs = stoichs, threshold = int(max_num))
                    
                    if cn_e:
                        for num in cn_r:
                            if tuple(reduce_formula.values()) == num:
                                return True

                        # print(cn_e)
                        # print(cn_r)
                        # print(ox_a, ox_b, ox_c)
                        # charge_neutral_count = charge_neutral_count + 1
                        # print('{0:3s}  {1:3s}  {2:3s}'.format(ele_a, ele_b, ele_c))
    print('Number of combinations = {0}'.format(charge_neutral_count))
    print("--- {0} seconds to run ---".format(time.time() - start_time)) 
    return False

def check_neutrality_3(formula):
    charge_neutral_count = 0
    comp = mg.Composition(formula)
    reduce_formula = comp.get_el_amt_dict()
    list_of_elements = list(reduce_formula.keys())
    stoichs = list(
                np.array(list(reduce_formula.values())).astype(np.int32)[:,np.newaxis]
            )
    max_num = max(reduce_formula.values())
    for i, ele_a in enumerate(list_of_elements):
        for ox_a in smact.Element(ele_a).oxidation_states:
            for j, ele_b in enumerate(list_of_elements[i+1:]):
                for ox_b in smact.Element(ele_b).oxidation_states:
                    for k, ele_c in enumerate(list_of_elements[i+j+2:]):
                        for ox_c in smact.Element(ele_c).oxidation_states:
                            
                            # Checks if the combination is charge neutral before printing it out! #                        
                            cn_e, cn_r = neutral_ratios([ox_a, ox_b, ox_c], stoichs = stoichs, threshold = int(max_num))
                            
                            if cn_e:
                                for num in cn_r:
                                    if tuple(reduce_formula.values()) == num:
                                        return True

                                                                # print(cn_e)
                                                                # print(cn_r)
                                                                # print(ox_a, ox_b, ox_c)
                                                                # charge_neutral_count = charge_neutral_count + 1
                                                                # print('{0:3s}  {1:3s}  {2:3s}'.format(ele_a, ele_b, ele_c))
    print('Number of combinations = {0}'.format(charge_neutral_count))
    print("--- {0} seconds to run ---".format(time.time() - start_time)) 
    return False

def check_neutrality_4(formula):
    charge_neutral_count = 0
    comp = mg.Composition(formula)
    reduce_formula = comp.get_el_amt_dict()
    list_of_elements = list(reduce_formula.keys())
    stoichs = list(
                np.array(list(reduce_formula.values())).astype(np.int32)[:,np.newaxis]
            )
    max_num = max(reduce_formula.values())
    for i, ele_a in enumerate(list_of_elements):
        for ox_a in smact.Element(ele_a).oxidation_states:
            for j, ele_b in enumerate(list_of_elements[i+1:]):
                for ox_b in smact.Element(ele_b).oxidation_states:
                    for k, ele_c in enumerate(list_of_elements[i+j+2:]):
                        for ox_c in smact.Element(ele_c).oxidation_states:
                            for m, ele_d in enumerate(list_of_elements[i+j+k+3:]):
                                for ox_d in smact.Element(ele_d).oxidation_states:
                            
                                    # Checks if the combination is charge neutral before printing it out! #                        
                                    cn_e, cn_r = neutral_ratios([ox_a, ox_b, ox_c, ox_d], stoichs = stoichs, threshold = int(max_num))
                                    
                                    if cn_e:
                                        for num in cn_r:
                                            if tuple(reduce_formula.values()) == num:
                                                return True

                                                                # print(cn_e)
                                                                # print(cn_r)
                                                                # print(ox_a, ox_b, ox_c)
                                                                # charge_neutral_count = charge_neutral_count + 1
                                                                # print('{0:3s}  {1:3s}  {2:3s}'.format(ele_a, ele_b, ele_c))
    print('Number of combinations = {0}'.format(charge_neutral_count))
    print("--- {0} seconds to run ---".format(time.time() - start_time)) 
    return False

def check_neutrality_5(formula):
    charge_neutral_count = 0
    comp = mg.Composition(formula)
    reduce_formula = comp.get_el_amt_dict()
    list_of_elements = list(reduce_formula.keys())
    stoichs = list(
                np.array(list(reduce_formula.values())).astype(np.int32)[:,np.newaxis]
            )
    max_num = max(reduce_formula.values())
    for i, ele_a in enumerate(list_of_elements):
        for ox_a in smact.Element(ele_a).oxidation_states:
            for j, ele_b in enumerate(list_of_elements[i+1:]):
                for ox_b in smact.Element(ele_b).oxidation_states:
                    for k, ele_c in enumerate(list_of_elements[i+j+2:]):
                        for ox_c in smact.Element(ele_c).oxidation_states:
                            for m, ele_d in enumerate(list_of_elements[i+j+k+3:]):
                                for ox_d in smact.Element(ele_d).oxidation_states:
                                    for n, ele_e in enumerate(list_of_elements[i+j+k+m+4:]):
                                        for ox_e in smact.Element(ele_e).oxidation_states:                             
                                            # Checks if the combination is charge neutral before printing it out! #                        
                                            cn_e, cn_r = neutral_ratios([ox_a, ox_b, ox_c, ox_d, ox_e], stoichs = stoichs, threshold = int(max_num))
                                            
                                            if cn_e:
                                                for num in cn_r:
                                                    if tuple(reduce_formula.values()) == num:
                                                        return True

                                                                # print(cn_e)
                                                                # print(cn_r)
                                                                # print(ox_a, ox_b, ox_c)
                                                                # charge_neutral_count = charge_neutral_count + 1
                                                                # print('{0:3s}  {1:3s}  {2:3s}'.format(ele_a, ele_b, ele_c))
    print('Number of combinations = {0}'.format(charge_neutral_count))
    print("--- {0} seconds to run ---".format(time.time() - start_time)) 
    return False

def check_neutrality_6(formula):
    charge_neutral_count = 0
    comp = mg.Composition(formula)
    reduce_formula = comp.get_el_amt_dict()
    list_of_elements = list(reduce_formula.keys())
    stoichs = list(
                np.array(list(reduce_formula.values())).astype(np.int32)[:,np.newaxis]
            )
    max_num = max(reduce_formula.values())
    for i, ele_a in enumerate(list_of_elements):
        for ox_a in smact.Element(ele_a).oxidation_states:
            for j, ele_b in enumerate(list_of_elements[i+1:]):
                for ox_b in smact.Element(ele_b).oxidation_states:
                    for k, ele_c in enumerate(list_of_elements[i+j+2:]):
                        for ox_c in smact.Element(ele_c).oxidation_states:
                            for m, ele_d in enumerate(list_of_elements[i+j+k+3:]):
                                for ox_d in smact.Element(ele_d).oxidation_states:
                                    for n, ele_e in enumerate(list_of_elements[i+j+k+m+4:]):
                                        for ox_e in smact.Element(ele_e).oxidation_states:
                                            for p, ele_f in enumerate(list_of_elements[i+j+k+m+n+5:]):
                                                for ox_f in smact.Element(ele_f).oxidation_states:
                                                    # Checks if the combination is charge neutral before printing it out! #                        
                                                    cn_e, cn_r = neutral_ratios([ox_a, ox_b, ox_c, ox_d, ox_e, ox_f], stoichs = stoichs, threshold = int(max_num))
                                                    
                                                    if cn_e:
                                                        for num in cn_r:
                                                            if tuple(reduce_formula.values()) == num:
                                                                return True

                                                                # print(cn_e)
                                                                # print(cn_r)
                                                                # print(ox_a, ox_b, ox_c)
                                                                # charge_neutral_count = charge_neutral_count + 1
                                                                # print('{0:3s}  {1:3s}  {2:3s}'.format(ele_a, ele_b, ele_c))
    print('Number of combinations = {0}'.format(charge_neutral_count))
    print("--- {0} seconds to run ---".format(time.time() - start_time)) 
    return False

def check_neutrality_7(formula):
    charge_neutral_count = 0
    comp = mg.Composition(formula)
    reduce_formula = comp.get_el_amt_dict()
    list_of_elements = list(reduce_formula.keys())
    stoichs = list(
                np.array(list(reduce_formula.values())).astype(np.int32)[:,np.newaxis]
            )
    max_num = max(reduce_formula.values())
    for element in reduce_formula.keys():
        print(len(smact.Element(element).oxidation_states), end = ",")
    for i, ele_a in enumerate(list_of_elements):
        for ox_a in smact.Element(ele_a).oxidation_states:
            for j, ele_b in enumerate(list_of_elements[i+1:]):
                for ox_b in smact.Element(ele_b).oxidation_states:
                    for k, ele_c in enumerate(list_of_elements[i+j+2:]):
                        for ox_c in smact.Element(ele_c).oxidation_states:
                            for m, ele_d in enumerate(list_of_elements[i+j+k+3:]):
                                for ox_d in smact.Element(ele_d).oxidation_states:
                                    for n, ele_e in enumerate(list_of_elements[i+j+k+m+4:]):
                                        for ox_e in smact.Element(ele_e).oxidation_states:
                                            for p, ele_f in enumerate(list_of_elements[i+j+k+m+n+5:]):
                                                for ox_f in smact.Element(ele_f).oxidation_states:
                                                    for q, ele_g in enumerate(list_of_elements[i+j+k+m+n+p+6:]):
                                                        for ox_g in smact.Element(ele_g).oxidation_states:
                                                            # Checks if the combination is charge neutral before printing it out! #                        
                                                            cn_e, cn_r = neutral_ratios([ox_a, ox_b, ox_c, ox_d, ox_e, ox_f, ox_g], stoichs = stoichs, threshold = int(max_num))
                                                            
                                                            if cn_e:
                                                                for num in cn_r:
                                                                    if tuple(reduce_formula.values()) == num:
                                                                        return True

                                                                # print(cn_e)
                                                                # print(cn_r)
                                                                # print(ox_a, ox_b, ox_c)
                                                                # charge_neutral_count = charge_neutral_count + 1
                                                                # print('{0:3s}  {1:3s}  {2:3s}'.format(ele_a, ele_b, ele_c))
    print('Number of combinations = {0}'.format(charge_neutral_count))
    print("--- {0} seconds to run ---".format(time.time() - start_time)) 
    return False

def check_neutrality_8(formula):
    charge_neutral_count = 0
    comp = mg.Composition(formula)
    reduce_formula = comp.get_el_amt_dict()
    list_of_elements = list(reduce_formula.keys())
    stoichs = list(
                np.array(list(reduce_formula.values())).astype(np.int32)[:,np.newaxis]
            )
    max_num = max(reduce_formula.values())
    for element in reduce_formula.keys():
        print(len(smact.Element(element).oxidation_states), end = ",")

    for i, ele_a in enumerate(list_of_elements):
        for ox_a in smact.Element(ele_a).oxidation_states:
            for j, ele_b in enumerate(list_of_elements[i+1:]):
                for ox_b in smact.Element(ele_b).oxidation_states:
                    for k, ele_c in enumerate(list_of_elements[i+j+2:]):
                        for ox_c in smact.Element(ele_c).oxidation_states:
                            for m, ele_d in enumerate(list_of_elements[i+j+k+3:]):
                                for ox_d in smact.Element(ele_d).oxidation_states:
                                    for n, ele_e in enumerate(list_of_elements[i+j+k+m+4:]):
                                        for ox_e in smact.Element(ele_e).oxidation_states:
                                            for p, ele_f in enumerate(list_of_elements[i+j+k+m+n+5:]):
                                                for ox_f in smact.Element(ele_f).oxidation_states:
                                                    for q, ele_g in enumerate(list_of_elements[i+j+k+m+n+p+6:]):
                                                        for ox_g in smact.Element(ele_g).oxidation_states:
                                                            for s, ele_h in enumerate(list_of_elements[i+j+k+m+n+p+q+7:]):
                                                                for ox_h in smact.Element(ele_h).oxidation_states:
                                                                    # Checks if the combination is charge neutral before printing it out! #                        
                                                                    cn_e, cn_r = neutral_ratios([ox_a, ox_b, ox_c, ox_d, ox_e, ox_f, ox_g, ox_h], stoichs = stoichs, threshold = int(max_num))
                                                                    
                                                                    if cn_e:
                                                                        for num in cn_r:
                                                                            if tuple(reduce_formula.values()) == num:
                                                                                return True

                                                                            # print(cn_e)
                                                                            # print(cn_r)
                                                                            # print(ox_a, ox_b, ox_c)
                                                                            # charge_neutral_count = charge_neutral_count + 1
                                                                            # print('{0:3s}  {1:3s}  {2:3s}'.format(ele_a, ele_b, ele_c))
    print('Number of combinations = {0}'.format(charge_neutral_count))
    print("--- {0} seconds to run ---".format(time.time() - start_time)) 
    return False

if __name__ == "__main__":
    print(check_neutrality("Ca6Cr2H1N6"))

    # print(check_neutrality_2("H2S"))
    # print(check_neutrality_3("C1Ho3Sn1"))
    # print(check_neutrality_4("Ba1O4Tl1V1"))
    # print(check_neutrality_5("Ba2Ca1Cu2Hg1O6"))
    # print(check_neutrality_6("F1H4Mg1Na1O6S1"))
    # print(check_neutrality_7("Mg2Mn2Cu1Ru1Yb1Pt1Au1"))
    # print(check_neutrality_8("F1H4Mg1Na1O10S1TiSi2")) La2Sn5