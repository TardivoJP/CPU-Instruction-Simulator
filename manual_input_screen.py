from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QScrollArea, QComboBox, QGridLayout
from instruction import Instruction
from instruction_list_processor import run_instructions

class ManualInputScreen(QWidget):
    def __init__(self, show_welcome_screen_callback, show_alert_box_callback, center_on_screen_callback):
        super().__init__()
        
        self.show_welcome_screen_callback = show_welcome_screen_callback
        self.show_alert_box_callback = show_alert_box_callback
        self.center_on_screen_callback = center_on_screen_callback
        
        self.instructions_array = []
        
        ## Master Layout
        self.manual_input_layout = QVBoxLayout()
        self.manual_input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        ## Add instructions master layout
        self.add_instructions_layout_container = QWidget()
        self.add_instructions_layout_container.setVisible(False)
        self.add_instructions_layout = QVBoxLayout()
        
        
        ### Add instructions header
        self.add_instructions_label = QLabel("<h3>Inserir instrucoes</h3>")
        self.add_instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.add_instructions_layout.addWidget(self.add_instructions_label)
        self.add_instructions_layout.addSpacing(10)
        
        
        ### Add instructions scroll area
        self.add_instructions_scroll_area = QScrollArea()
        self.add_instructions_scroll_area.setWidgetResizable(True)
        
        self.add_instructions_scroll_layout_container = QWidget()
        self.add_instructions_scroll_layout = QVBoxLayout()
        self.add_instructions_scroll_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        #### Add instructions list
        self.instructions_list_container = QWidget()
        self.instructions_list_layout = QGridLayout()
        self.instructions_list_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.instructions_list_container.setLayout(self.instructions_list_layout)
        self.add_instructions_scroll_layout.addWidget(self.instructions_list_container)
        
        self.add_instructions_scroll_layout_container.setLayout(self.add_instructions_scroll_layout)
        self.add_instructions_scroll_area.setWidget(self.add_instructions_scroll_layout_container)
        self.add_instructions_layout.addWidget(self.add_instructions_scroll_area)
        self.add_instructions_layout.addSpacing(10)
        
        
        ### Add instruction input
        self.instructions_list_add_item_container = QWidget()
        self.instructions_list_add_item_layout = QHBoxLayout()
        self.instructions_list_add_item_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.add_instructions_list_add_item_header_label = QLabel(f"{len(self.instructions_array)+1}")
        self.instructions_list_add_item_layout.addWidget(self.add_instructions_list_add_item_header_label)
        
        self.code_choice_box = QComboBox()
        self.code_choice_box.addItems(["000001", "000010", "000011", "000100", "000101", "000110", "000111", "001000", "001001", "001010", "001011", "001111", "001100"])
        self.instructions_list_add_item_layout.addWidget(self.code_choice_box)
        self.code_choice_box.currentIndexChanged.connect(self.on_main_combobox_changed)
        
        self.value_a_input = QLineEdit()
        self.value_a_input.setPlaceholderText("#pos")
        self.instructions_list_add_item_layout.addWidget(self.value_a_input)

        self.value_b_input = QLineEdit()
        self.value_b_input.setDisabled(True)
        self.instructions_list_add_item_layout.addWidget(self.value_b_input)
        
        self.confirm_add_list_add_item_button = QPushButton("Inserir")
        self.confirm_add_list_add_item_button.clicked.connect(self.insert_new_instruction)
        self.instructions_list_add_item_layout.addWidget(self.confirm_add_list_add_item_button)
        
        self.instructions_list_add_item_container.setLayout(self.instructions_list_add_item_layout)
        self.add_instructions_layout.addWidget(self.instructions_list_add_item_container)
        
        
        ### Add instructions back button
        self.add_instructions_back_button = QPushButton("Voltar")
        self.add_instructions_back_button.clicked.connect(self.show_add_instructions_view)
        self.add_instructions_layout.addWidget(self.add_instructions_back_button)
        
        self.add_instructions_layout_container.setLayout(self.add_instructions_layout)
        self.manual_input_layout.addWidget(self.add_instructions_layout_container)
        
        
        ## Menu view master layout
        self.menu_view_layout_container = QWidget()
        self.menu_view_layout_container.setVisible(True)
        self.menu_view_layout = QVBoxLayout()
        
        
        ### Menu view header
        self.menu_view_input_label = QLabel("<h2>Entrada manual de valores</h2>")
        self.menu_view_input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.menu_view_layout.addWidget(self.menu_view_input_label)
        
        
        ### Insert instructions button
        self.menu_view_input_insert_instructions_button = QPushButton("Inserir instrucoes")
        self.menu_view_input_insert_instructions_button.clicked.connect(self.show_add_instructions_view)
        self.menu_view_layout.addWidget(self.menu_view_input_insert_instructions_button)
        
        
        ### Run instructions button
        self.menu_view_run_instructions_button = QPushButton("Executar instrucoes")
        self.menu_view_run_instructions_button.clicked.connect(self.run_instructions_function)
        self.menu_view_layout.addWidget(self.menu_view_run_instructions_button)
        
        
        ### Back button
        self.menu_view_input_back_button = QPushButton("Voltar")
        self.menu_view_input_back_button.clicked.connect(self.show_welcome_screen_callback)
        self.menu_view_layout.addWidget(self.menu_view_input_back_button)
        
        self.menu_view_layout_container.setLayout(self.menu_view_layout)
        self.manual_input_layout.addWidget(self.menu_view_layout_container)
        
        
        ## Results view master layout
        self.results_view_layout_container = QWidget()
        self.results_view_layout_container.setVisible(False)
        self.results_view_layout = QVBoxLayout()
        
        
        ### Results view scroll area
        self.instructions_result_scroll_area = QScrollArea()
        self.instructions_result_scroll_area.setWidgetResizable(True)
        
        self.instructions_result_layout_container = QWidget()
        self.instructions_result_layout = QVBoxLayout()
        self.instructions_result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        #### MBR result
        self.mbr_result_label = QLabel("<h2>MBR Final</h2>")
        self.mbr_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.mbr_result_label)
        self.instructions_result_layout.addSpacing(10)
        
        self.mbr_result_value = QLabel()
        self.mbr_result_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.mbr_result_value)
        self.instructions_result_layout.addSpacing(20)
        
        
        #### Instructions log output
        self.instructions_log_output_label = QLabel("<h2>Instrucoes realizadas</h2>")
        self.instructions_log_output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.instructions_log_output_label)
        self.instructions_result_layout.addSpacing(10)
        
        self.instructions_log_output_value = QLabel()
        self.instructions_log_output_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.instructions_log_output_value)
        self.instructions_result_layout.addSpacing(20)
        
        
        #### Tape result output
        self.tape_result_output_label = QLabel("<h2>Fita final</h2>")
        self.tape_result_output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.tape_result_output_label)
        self.instructions_result_layout.addSpacing(10)
        
        self.tape_result_output_value = QLabel()
        self.tape_result_output_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.tape_result_output_value)
        
        
        self.instructions_result_layout_container.setLayout(self.instructions_result_layout)
        self.instructions_result_scroll_area.setWidget(self.instructions_result_layout_container)
        self.results_view_layout.addWidget(self.instructions_result_scroll_area)
        
        
        ## Results view back button
        self.results_view_back_button = QPushButton("Voltar")
        self.results_view_back_button.clicked.connect(self.show_menu_view)
        self.results_view_layout.addWidget(self.results_view_back_button)
        
        
        self.results_view_layout_container.setLayout(self.results_view_layout)
        self.manual_input_layout.addWidget(self.results_view_layout_container)
        
        
        self.setLayout(self.manual_input_layout)
        
        if not self.isMaximized:
            QTimer.singleShot(0, self.center_on_screen_callback)
        
    def show_menu_view(self): 
        self.results_view_layout_container.setVisible(False)
        self.menu_view_layout_container.setVisible(True)
        
    def show_add_instructions_view(self):
        if(self.add_instructions_layout_container.isVisible()):
            self.add_instructions_layout_container.setVisible(False)
            self.menu_view_layout_container.setVisible(True)
        else:
            self.menu_view_layout_container.setVisible(False)
            self.add_instructions_layout_container.setVisible(True)
            self.update_add_instructions_view()
            
            self.code_choice_box.setCurrentIndex(0)
        
            self.value_a_input.clear()
            self.value_a_input.setDisabled(False)
            self.value_a_input.setPlaceholderText("#pos")
            
            self.value_b_input.clear()
            self.value_b_input.setDisabled(True)
            self.value_b_input.setPlaceholderText("")
    
    def update_add_instructions_view(self):
        while self.instructions_list_layout.count():
            item = self.instructions_list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        self.add_instructions_list_header_instruction_label = QLabel(f"Instrucao")
        self.add_instructions_list_header_instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_list_layout.addWidget(self.add_instructions_list_header_instruction_label, 0, 0)
        
        self.add_instructions_list_header_code_label = QLabel(f"Codigo da Instrucao")
        self.add_instructions_list_header_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_list_layout.addWidget(self.add_instructions_list_header_code_label, 0, 1)
        
        self.add_instructions_list_header_operand_label = QLabel(f"Operandos")
        self.add_instructions_list_header_operand_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_list_layout.addWidget(self.add_instructions_list_header_operand_label, 0, 2, 1, 2)
        
        self.add_instructions_list_header_delete_label = QLabel(f"Remover?")
        self.add_instructions_list_header_delete_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_list_layout.addWidget(self.add_instructions_list_header_delete_label, 0, 4)
        
        for i in range(len(self.instructions_array)):
            self.add_instructions_list_item_pos_label = QLabel(f"{i+1}")
            self.add_instructions_list_item_pos_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.instructions_list_layout.addWidget(self.add_instructions_list_item_pos_label, (i+1), 0)
              
            self.add_instructions_list_item_code_label = QLabel(f"{self.instructions_array[i].code}")
            self.add_instructions_list_item_code_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.instructions_list_layout.addWidget(self.add_instructions_list_item_code_label, (i+1), 1)
            
            if(self.instructions_array[i].code not in ["001010", "001011", "001100"]):
                
                operand_title = ""
                
                if(self.instructions_array[i].code in ["000001", "000010", "000011", "000100", "000101", "000110", "001111"]):
                    operand_title = "pos"
                else:
                    operand_title = "lin"
                
                self.add_instructions_list_item_operand_a_label = QLabel(f"#{operand_title} {self.instructions_array[i].value_a}")
                self.add_instructions_list_item_operand_a_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.instructions_list_layout.addWidget(self.add_instructions_list_item_operand_a_label, (i+1), 2)
                    
                if(self.instructions_array[i].code == "000010"):
                    self.add_instructions_list_item_operand_b_label = QLabel(f"#dado {self.instructions_array[i].value_b}")
                    self.add_instructions_list_item_operand_b_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.instructions_list_layout.addWidget(self.add_instructions_list_item_operand_b_label, (i+1), 3)
                    
            self.add_instructions_list_item_delete_button = QPushButton("Remover")
            self.add_instructions_list_item_delete_button.clicked.connect(self.create_delete_button_callback(i))
            self.instructions_list_layout.addWidget(self.add_instructions_list_item_delete_button, (i+1), 4)
            
        self.add_instructions_list_add_item_header_label.setText(f"{len(self.instructions_array)+1}")
        
    def on_main_combobox_changed(self):
        selected_option = self.code_choice_box.currentText()
        
        if(selected_option not in ["001010", "001011", "001100"]):
            self.value_a_input.clear()
            self.value_a_input.setDisabled(False)
            
            operand_title = ""
            
            if(selected_option in ["000001", "000010", "000011", "000100", "000101", "000110", "001111"]):
                operand_title = "pos"
            else:
                operand_title = "lin"
            
            self.value_a_input.setPlaceholderText(f"#{operand_title}")
            
            if(selected_option == "000010"):
                self.value_b_input.clear()
                self.value_b_input.setDisabled(False)
                self.value_b_input.setPlaceholderText(f"#dado")
            else:
                self.value_b_input.clear()
                self.value_b_input.setDisabled(True)
                self.value_b_input.setPlaceholderText("")
        else:
            self.value_a_input.clear()
            self.value_a_input.setDisabled(True)
            self.value_a_input.setPlaceholderText("")
            
            self.value_b_input.clear()
            self.value_b_input.setDisabled(True)
            self.value_b_input.setPlaceholderText("")
            
    def insert_new_instruction(self):
        selected_option = self.code_choice_box.currentText()
        invalid_value = False
        
        if(selected_option not in ["001010", "001011", "001100"]):
            num_a = 0
            num_b = 0
            
            try:
                num_a = int(self.value_a_input.text())
            except ValueError:
                invalid_value = True
            
            if(not invalid_value):
                if(selected_option == "000010"):
                    try:
                        num_b = float(self.value_b_input.text())
                    except ValueError:
                        invalid_value = True
                    
                    if(not invalid_value):
                        self.instructions_array.append(Instruction(self.code_choice_box.currentText(), num_a, num_b))
                else:
                    self.instructions_array.append(Instruction(self.code_choice_box.currentText(), num_a))
        else:
            self.instructions_array.append(Instruction(self.code_choice_box.currentText()))
            
        if(invalid_value):
            self.show_alert_box_callback("Alerta!", f"Instrucao invalida, parametros devem ser numeros inteiros, ou decimal apenas no caso do dado em '000010'.")
        else:
            self.update_add_instructions_view()
        
    def remove_instruction(self, index):
        self.instructions_array.pop(index)
            
        self.update_add_instructions_view()
        
    def create_delete_button_callback(self, index):
        def callback():
            self.remove_instruction(index)
        return callback
    
    def run_instructions_function(self):
        self.menu_view_layout_container.setVisible(False)
        self.results_view_layout_container.setVisible(True)
        
        mbr, log, tape_display, out_of_bounds_error = run_instructions(self.instructions_array)
            
        if(out_of_bounds_error):
            self.show_alert_box_callback("Alerta!", f"Sequencia de instrucoes parada antes de sua conclusao, jump realizado para linha inexistente!")
        
        self.mbr_result_value.setText(str(mbr))
        self.tape_result_output_value.setText(''.join(tape_display))
                        
        if(len(log) == 0):
            self.instructions_log_output_value.setText("VAZIO")
        else:
            self.instructions_log_output_value.setText(''.join(log))
            
        self.results_view_layout_container.setVisible(True)