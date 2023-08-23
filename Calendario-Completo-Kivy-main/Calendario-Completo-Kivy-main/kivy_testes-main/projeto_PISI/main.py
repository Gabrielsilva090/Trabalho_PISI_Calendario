from kivy.lang import Builder
from kivymd.app import MDApp
from datetime import datetime, date
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.pickers import MDDatePicker
from datetime import datetime
from kivymd.uix.list import TwoLineAvatarIconListItem, ILeftBodyTouch
from kivymd.uix.selectioncontrol import MDCheckbox
from idiomas.en.strings import translations as en_translations
from idiomas.pt.strings import translations as pt_translations
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle 
from kivy.core.window import Window
from kivy.config import Config
from kivy.app import App
import locale 
locale.setlocale(locale.LC_ALL, '') #alterar a linguagem do aplicativo com a do usuário


class BackgroundColorApp(MDApp): #mudar o fundo do aplicativo
    def build(self):
        return Builder.load_file('background.kv')



from database import Database #salvar as informações e puxa-lás do database
db = Database()


class ListItemWithCheckbox(TwoLineAvatarIconListItem): #marcar os itens selecionados e retirar a seleção 

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def mark(self, check, the_list_item):
        if check.active:
            the_list_item.text = '[s]'+the_list_item.text+'[/s]'
            db.mark_task_as_complete(the_list_item.pk)
        else:
            the_list_item.text = the_list_item.text

    def delete_item(self, the_list_item): #deleta um item da lista 
        self.parent.remove_widget(the_list_item)
        db.delete_task(the_list_item.pk)

class LeftCheckbox(ILeftBodyTouch, MDCheckbox):
    pass

class DialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    def show_date_picker(self): #aparece o calendário 
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):

        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)


class MainApp(MDApp):

    task_list_dialog = None

    def build(self):
        self.theme_cls.primary_palette = "Purple" #tema geral do aplicativo
        self.icon = "calendario_logo.png"
    def show_task_dialog(self): #mostra a tela de dialógo quando apertar o botão de +
        if not self.task_list_dialog:
            self.task_list_dialog = MDDialog(title="Criar Tarefa", type="custom", content_cls=DialogContent())
        self.task_list_dialog.open()

    def on_start(self):
        try:
            completed_tasks, uncomplete_tasks = db.get_tasks()
            

        
            for task in uncomplete_tasks:
                    print("task :", task)
                    add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                    print(task[2])
                    date_object = task[2].rsplit(' ')  #retirar tasks que já passaram da data
                    print(date_object)
                    dia_at = date_object[1]
                    ano_at = date_object[3]
                    mes_str = date_object[2]

                    if mes_str == 'janeiro':
                        mes_at = '01'
                    elif mes_str == 'fevereiro':
                        mes_at = '02'
                    elif mes_str == 'março':
                        mes_at = '03'
                    elif mes_str == 'abril':
                        mes_at = '04'
                    elif mes_str == 'maio':
                        mes_at = '05'
                    elif mes_str == 'junho':
                        mes_at = '06'
                    elif mes_str == 'julho':
                        mes_at = '07'
                    elif mes_str == 'agosto':
                        mes_at = '08'
                    elif mes_str == 'setembro':
                        mes_at = '09'
                    elif mes_str == 'outubro':
                        mes_at = '10'
                    elif mes_str == 'novembro':
                        mes_at = '11'
                    elif mes_str == 'dezembro':
                        mes_at = '12'

                    due_date = datetime(int(ano_at), int(mes_at), int(dia_at))
                    if datetime.now() > due_date:
                        add_task.text = '[s]' + add_task.text + '[/s]'
                    self.root.ids.container.add_widget(add_task)

            
            for task in completed_tasks:
                    add_task = ListItemWithCheckbox(pk=task[0], text=task[1], secondary_text=task[2])
                    add_task.ids.check.active = True
                    print(task[2])
                    date_object = task[2].rsplit(' ')
                    print(date_object)
                    dia_at = date_object[1]
                    ano_at = date_object[3]
                    mes_str = date_object[2]

                    if mes_str == 'janeiro':
                        mes_at = '01'
                    elif mes_str == 'fevereiro':
                        mes_at = '02'
                    elif mes_str == 'março':
                        mes_at = '03'
                    elif mes_str == 'abril':
                        mes_at = '04'
                    elif mes_str == 'maio':
                        mes_at = '05'
                    elif mes_str == 'junho':
                        mes_at = '06'
                    elif mes_str == 'julho':
                        mes_at = '07'
                    elif mes_str == 'agosto':
                        mes_at = '08'
                    elif mes_str == 'setembro':
                        mes_at = '09'
                    elif mes_str == 'outubro':
                        mes_at = '10'
                    elif mes_str == 'novembro':
                        mes_at = '11'
                    elif mes_str == 'dezembro':
                        mes_at = '12'

                    due_date = datetime(int(ano_at), int(mes_at), int(dia_at))

                    if datetime.now() > due_date: 
                        add_task.text = '[s]' + add_task.text + '[/s]'
                    
                        self.root.ids.container.add_widget(add_task)
        
        except Exception as e:
            print(e)
            pass


    def close_dialog(self, *args):
        self.task_list_dialog.dismiss()

    def add_task(self, task, task_date): #função para adicionar tarefas
        created_task = db.create_task(task.text, task_date)
        print("created_task ", created_task)
        self.root.ids.container.add_widget(ListItemWithCheckbox(pk=created_task[0], text='[b]'+created_task[1]+'[/b]', secondary_text=created_task[2]))
        task.text = ''


if __name__ == "__main__":
    MainApp().run()
    
