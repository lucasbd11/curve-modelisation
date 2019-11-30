import math
import matplotlib.pyplot as plt
import numpy as np
import copy



def priority(calc, level_ = 0):
    
    
    calc_structured = []
    numbers = "0123456789."
    letters = "abcdefghijklmnopqrstuvwxyzABDCEFGHIJKLMNOPQRSTUVWXYZ"
    operators = "+*-/^"
    functions = ["cos","sin","exp","sqrt"]
    
    
    #level = 0
    in_progress = "none"
    index_jump = 0
    
    for index,char in enumerate(calc):
        if index >= index_jump:
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
                    index_jump = sub_calc_end
                            
            if char == "]":
                in_progress = "none"       
            if in_progress == "var" and char != "[":
                calc_structured[-1] += char
                    
    
    
            
    
            
            #print(index,char,in_progress)
            
            if char ==")":
                in_progress = ")"
        
    return calc_structured



def calculate_formula(formula,data_index,var_dict):
    
    temp_value = 0
    formula_bis = copy.copy(formula)
    
    functions = ["cos","sin","exp","sqrt"]
    vars = [i for i in var_dict]
    
    
    
    for index,value in enumerate(formula):
        if type(value) == list:
            answer = calculate_formula(formula[index],data_index,var_dict)
            if type(answer) == bool:
                return False
            else:
                formula_bis[index] = answer
    
    index_variation = 0
    formula = copy.copy(formula_bis)

    for index,value in enumerate(formula):
        if value == "cos":
            formula_bis[index-index_variation] = math.cos(float(formula_bis[index+(1-index_variation)]))
            del formula_bis[index+(1-index_variation)]
            index_variation +=1
            
        if value == "sin":
            formula_bis[index-index_variation] = math.sin(float(formula_bis[index+(1-index_variation)]))
            del formula_bis[index+(1-index_variation)]
            index_variation +=1
        
        if value == "sqrt":

            formula_bis[index-index_variation] = math.sqrt(float(formula_bis[index+(1-index_variation)]))
            del formula_bis[index+(1-index_variation)]
            index_variation +=1
        
        if value == "exp":
            formula_bis[index-index_variation] = math.exp(float(formula_bis[index+(1-index_variation)]))
            del formula_bis[index+(1-index_variation)]
            index_variation +=1
        
        try:
            var_index = vars.index(value)
            
            try:
                formula_bis[index-index_variation] = var_dict[value][data_index]
                
            except:
                return False
                
            
        except:
            pass
        


    
    formula = copy.copy(formula_bis)    
    index_variation = 0
    
    
    for index,value in enumerate(formula):
        if value == "^":
            formula_bis = formula_bis[:index-(1+index_variation)] + [float(formula_bis[index-(1+index_variation)])**float(formula_bis[index+(1-index_variation)])] + formula_bis[index+(2-index_variation):]
            index_variation += 2
    
    
    index_variation = 0
    formula = copy.copy(formula_bis)
    
   
    
    for index,value in enumerate(formula):
        if value == "/":

            formula_bis = formula_bis[:index-(1+index_variation)] + [float(formula_bis[index-(1+index_variation)])/float(formula_bis[index+(1-index_variation)])] + formula_bis[index+(2-index_variation):]
            index_variation += 2
        
        if value == "*":
            
            formula_bis = formula_bis[:index-(1+index_variation)] + [float(formula_bis[index-(1+index_variation)])*float(formula_bis[index+(1-index_variation)])] + formula_bis[index+(2-index_variation):]
            index_variation += 2
            
            
    formula = copy.copy(formula_bis)
    index_variation = 0
    
    for index,value in enumerate(formula):
        if value == "+":
            
            formula_bis = formula_bis[:index-(1+index_variation)] + [float(formula_bis[index-(1+index_variation)])+float(formula_bis[index+(1-index_variation)])] + formula_bis[index+(2-index_variation):]
            index_variation += 2
        if value == "-":
            formula_bis = formula_bis[:index-(1+index_variation)] + [float(formula_bis[index-(1+index_variation)])-float(formula_bis[index+(1-index_variation)])] + formula_bis[index+(2-index_variation):]
            index_variation += 2
    
    
    
    return float(formula_bis[0])
        
    
def calculate_var(var,var_dict):
    formula_save = var_dict[var][0]
    answer = 1.0
    del var_dict[var]
    var_dict[var] = [formula_save]
    
    
    var_index = 1
    while type(answer) == float:
        answer = calculate_formula(priority(var_dict[var][0]),var_index,var_dict)
        if type(answer) == float:
            var_dict[var] += [answer]
            var_index += 1
    return var_dict
    
    

def menu(options_list):
    for index,option in enumerate(options_list):
        print(str(index+1)+" - " + option)
    answer = int(input(">"))
    return options_list[answer-1]

var_dict = {}
curve_dict = {}


def affine_modelisation(var_x,var_y):
    
    max_len = min(len(var_x),len(var_y))
    a = 1
    b = 0
    var_x = var_x[:max_len]
    var_y = var_y[:max_len]
    detla = -1
    
    squared_error_temp = 0
    for i in range(max_len):
        squared_error_temp += (var_y[i]-((a)*var_x[i]+b))**2
    
    list_param = [[0.01,0.01],[0.01,-0.01],[-0.01,0.01],[-0.01,-0.01],[-0.01,0],[0.01,0],[0,0.01],[0,-0.01]]
    
    while detla<0:
        squared_error = [0,0,0,0,0,0,0,0]
        for index in range(len(list_param)):
            for i in range(max_len):
                squared_error[index] += (var_y[i]-((a+list_param[index][0])*var_x[i]+b+list_param[index][1]))**2
        detla = min(squared_error)-squared_error_temp
        if detla<0:
            a += list_param[squared_error.index(min(squared_error))][0]
            b += list_param[squared_error.index(min(squared_error))][1]
            squared_error_temp = min(squared_error)
        

    return (a,b)
        


#calc = "2*[test]+sqrt([test2])"
#calc = "4*sqrt(9)+exp(2)"

#print(priority(calc))

#print(calculate_formula(priority(calc),1,var_dict))


print("Programme de modélisation de courbes")
print("Version 1.0")



while True:
    
    answer = menu(["créer une nouvelle variable","éditer une variable","Configurer le graphique","Afficher le graphique"])
    
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
        
        print("Pour faire référence à une variable merci de la mettre entre [] (listes des fonctions: cos,sin,exp,sqrt)\n")
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
                    var_dict[var_name] += [float(input_value)]
                except:
                    pass
        else:
            var_dict[var_name] += [formula_answer]
            var_dict = calculate_var(var_name,var_dict)
    
    if answer == "éditer une variable":
        print("Liste des variables à éditer:")
        for key in var_dict:
            if var_dict[key][0] == "none":
                print("-" + key + " (donnés)")
            else:
                print("-" + key + " (formule)")
        
        selected_var = input(">")
        
        print("Liste des options:")

        if var_dict[selected_var][0] == "none":
            answer = menu(["éditer les valeurs","supprimer la variable","visualiser les donnés","Retour"])
            
            if answer == "éditer les valeurs":   
                for index,value in enumerate(var_dict[selected_var][1:]):
                    print("("+str(index+1)+") " + str(value))
                
                print("Numéro du début de la séquence de valeur à éditer: (entrez 'stop' pour arrêter)")
                
                index = int(input(">"))
                
                input_value = "0"
                
                while input_value != "stop":
                    input_value = input("("+str(index)+")>")
                    
                    try:
                        var_dict[selected_var][index] = float(input_value)
                    except:
                        try:
                            var_dict[selected_var] += [float(input_value)]
                        except:
                            pass
                    index +=1
    
    
            if answer == "supprimer la variable":
                del var_dict[selected_var]
            
            if answer == "visualiser les donnés":
                for index,value in enumerate(var_dict[selected_var][1:]):
                    print("("+str(index+1)+") " + str(value))        
        
        else:
            answer = menu(["éditer la formule","supprimer la variable","Retour"])
            if answer == "éditer la formule":
                print("Ancienne formule:")
                print(var_dict[selected_var][0])
                print("Entrez la nouvelle formule:")
                var_dict[selected_var][0] = input(">")
            
            if answer == "supprimer la variable":
                del var_dict[selected_var]
                
        

            


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
            
            print("Couleur de la courbe (ex: blue/red/green...)")
            curve_dict[curve_name] += [input(">")]
            
        
        
        if answer == "Modéliser une courbe":
            if len(curve_dict)>0:
                
                print("Modéliser une courbe:")
                modelised_curve = menu([key for key in curve_dict])
                
                print("Modèle à utiliser:")
                
                model_used = menu(["Fonction affine"])
                
                if model_used == "Fonction affine":
                    a,b = affine_modelisation(var_dict[curve_dict[modelised_curve][0]][1:],var_dict[curve_dict[modelised_curve][1]][1:])
                    print("Fonction trouvée:")
                    print("a=",round(a,2))
                    print("b=",round(b,2))
                    #(max(var_dict[curve_dict[modelised_curve][0]][1:])-min(var_dict[curve_dict[modelised_curve][1]][1:]))*50
                    
                    x = np.linspace(int(min(var_dict[curve_dict[modelised_curve][0]][1:])), int(max(var_dict[curve_dict[modelised_curve][0]][1:])),int((max(var_dict[curve_dict[modelised_curve][0]][1:])-min(var_dict[curve_dict[modelised_curve][1]][1:]))*50))
                    
                    plt.plot(x, a*x+b, label='Model de: '+ modelised_curve)
            
            
            else:
                print("Aucune courbe existante")
        
        if answer == "Retirer une courbe":
            print("\nListe des courbes existantes:")
            for i in curve_dict:
                print("-"+i)
            print("\nEntrez le nom d'une courbe à retirer:'")
            del curve_dict[input(">")]
        
        if answer == "Configuer les axes":
            print("Nom de l'axe des x:'")
            plt.xlabel(input(">"))
            print("Nom de l'axe des y:'")
            plt.ylabel(input(">"))
        
        if answer == "Nom du graphique":
            print("Nom du graphique:'")
            plt.title(input(">"))

    if answer == "Afficher le graphique":
        
        for curve_i in curve_dict:
            max_len = min(len(var_dict[curve_dict[curve_i][0]][1:]),len(var_dict[curve_dict[curve_i][1]][1:]))+1
            
            plt.scatter(var_dict[curve_dict[curve_i][0]][1:max_len],var_dict[curve_dict[curve_i][1]][1:max_len], c = curve_dict[curve_i][2], label = curve_i,marker="x")
        
        plt.legend()
        plt.show()

