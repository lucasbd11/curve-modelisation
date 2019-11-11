import math
import matplotlib.pyplot as plt
import numpy as np
import copy



def priority(calc, level_ = 0):
    
    
    calc_structured = []
    numbers = "0123456789."
    letters = "abcdefghijklmnoqrstuvwxyz"
    operators = "+*-/^"
    functions = ["cos","sin","exp","sqrt"]
    
    
    #level = 0
    in_progress = "none"
    
    for index,char in enumerate(calc):
        
        if char == "[":
            in_progress = "var"
            calc_structured += [""]

        if(in_progress != "(") and in_progress != "var":
            
            
            if letters.find(char) > -1:
                if in_progress == "function":
                    calc_structured[-1] += char
                else:
                    calc_structured += [char]
                    in_progress = "function"
            
            
            
            if numbers.find(char) > -1:
                if in_progress == "number":
                    calc_structured[-1] += char
                else:
                    calc_structured += [char]
                    in_progress = "number"
            
            
            if operators.find(char) > -1:
                calc_structured += [char]
                in_progress = "operation"
            
            if char =="(":
                in_progress = "("
                level = 0
                locked = False
                
                for index_bis,char_bis in enumerate(calc[index:]):

                    
                    if char_bis == "(":
                        level += 1
                    if char_bis == ")":
                        level -= 1
                    
                    if level <= 0 and locked == False:
                        locked = True
                        sub_calc_end = index_bis + index
                
                calc_structured += [priority(calc[index+1:sub_calc_end])]            
        if char == "]":
            in_progress = "none"       
        if in_progress == "var" and char != "[":
            calc_structured[-1] += char
                   


        

        
        #print(index,char,in_progress)
        
        if char ==")":
            in_progress = ")"
        
    return calc_structured



def calculate_formula(formula,*var_dict):
    
    temp_value = 0
    formula_bis = copy.copy(formula)
    
    

    for index,value in enumerate(formula):
        if type(value) == list:
            formula_bis[index] = calculate_formula(formula[index])
       
       
    
    formula = copy.copy(formula_bis)    
    for index,value in enumerate(formula):
        if value == "^":
            formula_bis = formula_bis[:index-1] + [int(formula_bis[index-1])**int(formula_bis[index+1])] + formula_bis[index+2:]
    
    formula = copy.copy(formula_bis)
    
    for index,value in enumerate(formula):
        if value == "/":
            formula_bis = formula_bis[:index-1] + [int(formula_bis[index-1])/int(formula_bis[index+1])] + formula_bis[index+2:]
        if value == "*":
            formula_bis = formula_bis[:index-1] + [int(formula_bis[index-1])*int(formula_bis[index+1])] + formula_bis[index+2:]
            
    formula = copy.copy(formula_bis)
            
    for index,value in enumerate(formula):
        if value == "+":
            formula_bis = formula_bis[:index-1] + [int(formula_bis[index-1])+int(formula_bis[index+1])] + formula_bis[index+2:]
        if value == "-":
            formula_bis = formula_bis[:index-1] + [int(formula_bis[index-1])-int(formula_bis[index+1])] + formula_bis[index+2:]
    
    return formula_bis[0]
        
    
    
    

def menu(options_list):
    for index,option in enumerate(options_list):
        print(str(index+1)+" - " + option)
    answer = int(input(">"))
    return options_list[answer-1]

var_dict = {}
curve_dict = {}







calc = "4^2*(5+(2/3*5))/4"
print(priority(calc))

print(calculate_formula(priority(calc)))





1/0


print("Programme de modélisation de courbes")
print("Version 1.0")



while True:
    
    answer = menu(["créer une nouvelle variable","éditer une variable","Configurer le graphique","Afficher le graphique","modéliser une courbe"])
    
    if answer == "créer une nouvelle variable":
        
        print("\nNom de la variable:")
        var_name = input(">")
        var_dict[var_name] = []
        print("\nFormule de la variable ? (Pour ne mettre que des valeurs rentrez 'none'")
        
        print("Liste des variables disponibles:")
        
        for key in var_dict:
            if key == var_name:
                print("-" + key + "(inutilisable)")
            else:
                print("-" + key)
        print("\n")
        
        formula_answer = input(">")
        
        if formula_answer == "none":
            var_dict[var_name] += ["none"]
            
            var_index = 1
            
            print("\nEntrez les valeurs une par une, et écrivez 'stop' pour arrêter:")
            input_value = "0"
            
            while input_value != "stop":
                input_value = input("("+str(var_index)+")>")
                var_index +=1
                try:
                    var_dict[var_name] += [int(input_value)]
                except:
                    pass
        else:
            var_dict[var_name] += [formula_answer]
    
    if answer == "éditer une variable":
        print("Liste des variables à éditer:")
        for key in var_dict:
            if var_dict[key][0] == "none":
                print("-" + key + " (donnés)")
            else:
                print("-" + key + " (formule)")
        
        selected_var = input(">")
        
        print("Liste des options:")
        
        if var_dict[selected_var][0] != "none":
            answer = menu(["éditer la formule","supprimer la variable","visualiser les donnés","Retour"])
            if answer == "éditer la formule":
                print("Ancienne formule:")
                print(var_dict[selected_var][0])
                print("Entrez la nouvelle formule:")
                var_dict[selected_var][0] = input(">")
            
            if answer == "supprimer la variable":
                del var_dict[selected_var]
                
            if answer == "visualiser les donnés":
                for index,value in enumerate(var_dict[selected_var][1:]):
                    print("("+str(index+1)+") " + str(value))
        
        if var_dict[selected_var][0] == "none":
            answer = menu(["éditer les valeurs","supprimer la variable","visualiser les donnés","Retour"])
            
            if answer == "éditer les valeurs":   
                for index,value in enumerate(var_dict[selected_var][1:]):
                    print("("+str(index+1)+") " + str(value))
                
                print("Numéro du début de la séquence de valeur à éditer: (entrez 'stop' pour arrêter)")
                
                index = int(input(">"))-1
                
                input_value = "0"
                
                while input_value != "stop":
                    input_value = input("("+str(index+1)+")>")
                    
                    try:
                        var_dict[selected_var][index] = int(input_value)
                    except:
                        try:
                            var_dict[selected_var] += [int(input_value)]
                        except:
                            pass
                    index +=1
    
    
            if answer == "supprimer la variable":
                del var_dict[selected_var]
            
            if answer == "visualiser les donnés":
                for index,value in enumerate(var_dict[selected_var][1:]):
                    print("("+str(index+1)+") " + str(value))
            
    if answer == "Configurer le graphique":
        print("ok")
        answer = menu(["Ajouter une courbe","Modéliser une courbe","Retirer une courbe","Configuer les axes","Nom du graphique","Retour"])
        
        if answer == "Ajouter une courbe":
            
            print("Nom de la courbe:")
            curve_name = input(">")
            curve_dict[curve_name] = []
            
            print("Liste des variables disponibles:")
            
            for key in var_dict:
                    print("-" + key)
            
            print("Variable en x:")
            curve_var_x = input(">")
            curve_dict[curve_name] += [curve_var_x]
            
            print("Variable en y:")
            curve_var_y = input(">")
            curve_dict[curve_name] += [curve_var_y]
            
        
        
        if answer == "Modéliser une courbe":
            if len(curve_dict)>0:
                
                print("Modéliser une courbe:")
                modelised_curve = menu([key for key in curve_dict])
                
                print("Modèle à utiliser:")
                
                model_used = menu(["Fonction affine"])
                
                if model_used == "Fonction affine":
                    pass
            
            
            else:
                print("Aucune courbe existante")
                    


print(answer)

