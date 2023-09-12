from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QScrollArea, QFileDialog
from PyQt6.QtGui import QGuiApplication
from instruction import Instruction
from instruction_list_processor import run_instructions

class FileInputScreen(QWidget):
    def __init__(self, show_welcome_screen_callback, show_alert_box_callback, center_on_screen_callback):
        super().__init__()
        
        self.show_welcome_screen_callback = show_welcome_screen_callback
        self.show_alert_box_callback = show_alert_box_callback
        self.center_on_screen_callback = center_on_screen_callback
        
        self.instructions_array = []
        
        ## Screen dimensions
        screen = QGuiApplication.primaryScreen()
        screen_size = screen.availableSize()
        
        
        ## Master Layout
        self.master_layout = QVBoxLayout()
        
        self.file_input_scroll_area = QScrollArea()
        self.file_input_scroll_area.setWidgetResizable(True)
        self.file_input_scroll_area.setMinimumWidth(int(screen_size.width() * 0.70))
        self.file_input_scroll_area.setMinimumHeight(int(screen_size.height() * 0.70))
        
        self.file_input_container = QWidget()
        self.file_input_layout = QVBoxLayout()
        self.file_input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        
        ## Manual Input Screen Header
        self.file_input_label = QLabel("<h2>Entrada de valores por arquivo</h2>")
        self.file_input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_input_layout.addWidget(self.file_input_label)
        
        
        ## Text box input
        self.file_input_text_box = QTextEdit()
        self.file_input_text_box.setPlaceholderText(f"Cole o texto da tabela de transicao aqui...")
        self.file_input_text_box.setMinimumHeight(int(screen_size.height() * 0.50))
        self.file_input_layout.addWidget(self.file_input_text_box)
        
        
        ## Confirm button
        self.file_input_confirm_button = QPushButton("Confirmar")
        self.file_input_confirm_button.clicked.connect(self.get_data)
        self.file_input_layout.addWidget(self.file_input_confirm_button)
        
        ## Open file button
        self.file_input_open_file_button = QPushButton("Abrir arquivo")
        self.file_input_open_file_button.clicked.connect(self.open_file_button)
        self.file_input_layout.addWidget(self.file_input_open_file_button)
        
        ## Back button
        self.file_input_back_button = QPushButton("Voltar")
        self.file_input_back_button.clicked.connect(lambda: self.show_welcome_screen_callback())
        
        self.file_input_layout.addWidget(self.file_input_back_button)
                
        
        ## Result scroll area
        self.instructions_result_scroll_area = QScrollArea()
        self.instructions_result_scroll_area.setVisible(False)
        self.instructions_result_scroll_area.setWidgetResizable(True)
        self.instructions_result_scroll_area.setMinimumHeight(int(screen_size.height() * 0.50))
        
        self.instructions_result_layout_container = QWidget()
        self.instructions_result_layout = QVBoxLayout()
        self.instructions_result_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        ## MBR result
        self.mbr_result_label = QLabel("<h2>MBR Final</h2>")
        self.mbr_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.mbr_result_label)
        self.instructions_result_layout.addSpacing(10)
        
        self.mbr_result_value = QLabel()
        self.mbr_result_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.mbr_result_value)
        self.instructions_result_layout.addSpacing(20)
        
        
        ## Instructions log output
        self.instructions_log_output_label = QLabel("<h2>Instrucoes realizadas</h2>")
        self.instructions_log_output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.instructions_log_output_label)
        self.instructions_result_layout.addSpacing(10)
        
        self.instructions_log_output_value = QLabel()
        self.instructions_log_output_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.instructions_log_output_value)
        self.instructions_result_layout.addSpacing(20)
        
        
        ## Tape result output
        self.tape_result_output_label = QLabel("<h2>Fita final</h2>")
        self.tape_result_output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.tape_result_output_label)
        self.instructions_result_layout.addSpacing(10)
        
        self.tape_result_output_value = QLabel()
        self.tape_result_output_value.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instructions_result_layout.addWidget(self.tape_result_output_value)
        
        
        self.instructions_result_layout_container.setLayout(self.instructions_result_layout)
        self.instructions_result_scroll_area.setWidget(self.instructions_result_layout_container)
        self.file_input_layout.addWidget(self.instructions_result_scroll_area)
        
        
        self.file_input_container.setLayout(self.file_input_layout)
        self.file_input_scroll_area.setWidget(self.file_input_container)
        
        self.master_layout.addWidget(self.file_input_scroll_area)
        
        self.setLayout(self.master_layout)
        
        if not self.isMaximized:
            QTimer.singleShot(0, self.center_on_screen_callback)
        
    def open_file_button(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("Sequencias de instrucoes (*.txt)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            selected_file = file_dialog.selectedFiles()[0]
            
            with open(selected_file, "r") as file:
                raw_text = file.read()
                
            self.file_input_text_box.setText(raw_text)
                
            lines = raw_text.split('\n')
            self.parse_instructions(lines)
        
    def get_data(self):
        raw_text = self.file_input_text_box.toPlainText()
        lines = raw_text.split('\n')
        self.parse_instructions(lines)
        
    def parse_instructions(self, lines):
        self.instructions_array.clear()
        error_triggered = False
        
        for i in range(len(lines)):
            line_value = lines[i].split(",")
            num_a = 0
            num_b = 0
            
            if(line_value[0] not in ["000001", "000010", "000011", "000100", "000101", "000110", "000111", "001000", "001001", "001010", "001011", "001111", "001100"]):
                self.show_alert_box_callback("Alerta!", f"Sequencia de instrucoes invalida! Instrucao da linha {(i+1)} nao possui codigo valido!")
                error_triggered = True
                break
            
            if(line_value[0] in ["000001", "000010", "000011", "000100", "000101", "000110", "000111", "001000", "001001", "001111"]):
                try:
                    num_a = int(line_value[1])
                except ValueError:
                    self.show_alert_box_callback("Alerta!", f"Sequencia de instrucoes invalida! Instrucao da linha {(i+1)} nao possui valor valido!")
                    error_triggered = True
                    break
                    
                if(line_value[0] == "000010"):
                    try:
                        num_b = float(line_value[2])
                    except ValueError:
                        self.show_alert_box_callback("Alerta!", f"Sequencia de instrucoes invalida! Instrucao da linha {(i+1)} nao possui valor valido!")
                        error_triggered = True
                        break
                    
                    self.instructions_array.append(Instruction(line_value[0], num_a, num_b))
                else:
                    self.instructions_array.append(Instruction(line_value[0], num_a))
            else:
                self.instructions_array.append(Instruction(line_value[0]))
        
        if(not error_triggered):
            mbr, log, tape_display, out_of_bounds_error = run_instructions(self.instructions_array)
            
            if(out_of_bounds_error):
                self.show_alert_box_callback("Alerta!", f"Sequencia de instrucoes parada antes de sua conclusao, jump realizado para linha inexistente!")
                
            self.mbr_result_value.setText(str(mbr))
            self.tape_result_output_value.setText(''.join(tape_display))
            
            if(len(log) == 0):
                self.instructions_log_output_value.setText("VAZIO")
            else:
                self.instructions_log_output_value.setText(''.join(log))
                
            self.instructions_result_scroll_area.setVisible(True)
        else:
            self.instructions_result_scroll_area.setVisible(False)