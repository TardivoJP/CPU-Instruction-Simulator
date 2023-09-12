from math import sqrt

def run_instructions(instructions_array):
    greatest_pos_value = 0
    
    for i in range(len(instructions_array)):
        if(instructions_array[i].code in ["000001", "000010", "000011", "000100", "000101", "000110", "001111"]):
            if(instructions_array[i].value_a > greatest_pos_value):
                greatest_pos_value = instructions_array[i].value_a 
    
    mbr = 0
    tape = [0.0] * (greatest_pos_value + 1)
    log = []
    tape_display = []
    current_instruction = 0
    
    out_of_bounds_error = False

    while(current_instruction < len(instructions_array)):
        current_instruction_code = instructions_array[current_instruction].code
        
        match current_instruction_code:
            case "000001": 
                mbr = tape[instructions_array[current_instruction].value_a]
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append(f"MBR recebeu o valor {tape[instructions_array[current_instruction].value_a]:.1f} da posicao {instructions_array[current_instruction].value_a}\n")
                log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "000010": 
                tape[instructions_array[current_instruction].value_a] = instructions_array[current_instruction].value_b
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append(f"A posicao {instructions_array[current_instruction].value_a} recebeu o valor {instructions_array[current_instruction].value_b:.1f}\n\n")
            case "000011":
                mbr += tape[instructions_array[current_instruction].value_a]
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append(f"MBR teve seu valor adionado por {tape[instructions_array[current_instruction].value_a]:.1f} da posicao {instructions_array[current_instruction].value_a}\n")
                log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "000100":
                mbr -= tape[instructions_array[current_instruction].value_a]
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append(f"MBR teve seu valor subtraido por {tape[instructions_array[current_instruction].value_a]:.1f} da posicao {instructions_array[current_instruction].value_a}\n")
                log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "000101":
                mbr *= tape[instructions_array[current_instruction].value_a]
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append(f"MBR teve seu valor multiplicado por {tape[instructions_array[current_instruction].value_a]:.1f} da posicao {instructions_array[current_instruction].value_a}\n")
                log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "000110":
                mbr /= tape[instructions_array[current_instruction].value_a]
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append(f"MBR teve seu valor dividido por {tape[instructions_array[current_instruction].value_a]:.1f} da posicao {instructions_array[current_instruction].value_a}\n")
                log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "000111":
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append(f"Jump realizado para a linha {instructions_array[current_instruction].value_a}\n\n")
                current_instruction = ((instructions_array[current_instruction].value_a) - 2)
            case "001000":
                if(mbr == 0):
                    log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                    log.append(f"Jump realizado para a linha {instructions_array[current_instruction].value_a}\n")
                    log.append(f"MBR atual e {mbr:.1f}\n\n")
                    current_instruction = ((instructions_array[current_instruction].value_a) - 2)
                else:
                    log.append(f"Operacao {instructions_array[current_instruction].code} NAO realizada!\n")
                    log.append(f"Jump para a linha {instructions_array[current_instruction].value_a} somente e executado caso MBR for 0\n")
                    log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "001001":
                if(mbr < 0):
                    log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                    log.append(f"Jump realizado para a linha {instructions_array[current_instruction].value_a}\n")
                    log.append(f"MBR atual e {mbr:.1f}\n\n")
                    current_instruction = ((instructions_array[current_instruction].value_a) - 2)
                else:
                    log.append(f"Operacao {instructions_array[current_instruction].code} NAO realizada!\n")
                    log.append(f"Jump para a linha {instructions_array[current_instruction].value_a} somente e executado caso MBR for negativo\n")
                    log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "001010":
                mbr = sqrt(mbr)
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append("Novo valor de MBR e sua raiz quadrada\n")
                log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "001011":
                mbr *= (-1)
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append("MBR foi multiplicado por -1 para trocar seu sinal\n")
                log.append(f"MBR atual e {mbr:.1f}\n\n")
            case "001111":
                tape[instructions_array[current_instruction].value_a] = mbr
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append(f"A posicao {instructions_array[current_instruction].value_a} recebeu o valor {mbr:.1f} do MBR\n\n")
            case "001100":
                log.append(f"Operacao {instructions_array[current_instruction].code} realizada\n")
                log.append("Nada foi feito\n\n")
        
        current_instruction += 1
        
        if(current_instruction < 0 or current_instruction > len(instructions_array)):
            out_of_bounds_error = True
            break
    
    for i in range(len(tape)):
        tape_display.append(str(str(i) + ": " + str(tape[i]) + " - "))
        if(i % 15 == 0):
            tape_display.append("\n")
    
    if(out_of_bounds_error):
        log.append("Operacao parada neste ponto. Linha do jump inexistente\n")
        return mbr, log, tape_display, True
        
    return mbr, log, tape_display, False