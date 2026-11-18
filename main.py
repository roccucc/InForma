import json
import os
from datetime import date, datetime, timedelta

from kivy.app import App
from kivy.cache import Cache
from kivy.graphics import Color, Ellipse, Line, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.core.window import Window


BG = (0.035, 0.055, 0.09, 1)
CARD = (0.075, 0.105, 0.16, 1)
CARD_ALT = (0.10, 0.14, 0.21, 1)
TEXT = (0.94, 0.96, 1, 1)
MUTED = (0.60, 0.66, 0.76, 1)
ACCENT = (0.52, 0.46, 1, 1)
MINT = (0.34, 0.88, 0.72, 1)
RED = (1, 0.39, 0.43, 1)


EXERCISES = {
    "Petto": [
        "Panca piana bilanciere", "Panca inclinata bilanciere",
        "Panca declinata bilanciere", "Panca piana manubri",
        "Panca inclinata manubri", "Panca declinata manubri",
        "Chest press macchina", "Chest press inclinata",
        "Distensioni manubri presa neutra", "Croci ai cavi alti",
        "Croci ai cavi bassi", "Croci ai cavi da sdraiato",
        "Croci manubri panca piana", "Croci manubri panca inclinata",
        "Pec deck", "Push-up", "Push-up inclinati",
        "Push-up con sovraccarico", "Dip alle parallele (petto)",
        "Pullover manubrio", "Squeeze press manubri", "Distensioni manubri panca inclinata",
    ],
    "Schiena": [
        "Stacco da terra", "Stacco rumeno", "Stacco sumo",
        "Rematore bilanciere", "Rematore manubrio", "Rematore chest-supported",
        "Rematore al cavo basso", "Rematore T-bar", "Pulley basso",
        "Lat machine presa larga", "Lat machine presa stretta",
        "Lat machine presa inversa", "Lat machine unilaterale",
        "Trazioni presa prona", "Trazioni presa supina",
        "Trazioni assistite", "Chin-up", "Pulldown braccia tese",
        "Pullover ai cavi", "Seal row", "Meadows row",
        "Back extension", "Iperestensioni", "Good morning",
        "Scrollate bilanciere", "Scrollate manubri", "iperestensioni su panca inclinata", "pull up", "Rematore manubrio al dorsy bar",
    ],
    "Spalle": [
        "Military press bilanciere", "Shoulder press manubri",
        "Arnold press", "Shoulder press macchina",
        "Alzate laterali manubri", "Alzate laterali al cavo basso",
        "Alzate laterali macchina", "Alzate frontali manubri",
        "Alzate frontali bilanciere", "Face pull",
        "Reverse fly ai cavi", "Reverse pec deck",
        "Tirate al mento bilanciere", "Landmine press",
        "Upright row ai cavi", "Y-raise", "Distensioni seduto dietro la nuca multipower", "deltoidi posteriori al cavo singolo",
    ],
    "Bicipiti": [
        "Curl bilanciere", "Curl bilanciere EZ", "Curl manubri alternato",
        "Curl manubri seduto", "Curl a martello", "Curl a martello ai cavi",
        "Curl preacher bilanciere EZ", "Curl preacher manubrio",
        "Curl ai cavi bassi", "Curl ai cavi alti",
        "Curl concentrato", "Curl spider", "Curl su panca inclinata",
        "Curl al cavo con barra", "Zottman curl","Curl a martello ai cavi bassi", "Curl con spalla estesa al cavo basso", "Curl con sbarra a z presa stretta",
    ],
    "Tricipiti": [
        "Pushdown ai cavi incrociati", "Pushdown corda", "Pushdown presa inversa",
        "French press bilanciere EZ", "French press manubri",
        "Estensioni sopra la testa ai cavi", "Estensioni manubrio sopra la testa",
        "Skull crusher", "Panca presa stretta", "Dip alle parallele (tricipiti)",
        "Kickback manubrio", "Kickback ai cavi", "JM press", "push up su rialzo", "Pull-over con manubrio su panca perpendicolare",
    ],
    "Gambe": [
        "Squat bilanciere", "Squat frontale", "Goblet squat",
        "Hack squat", "Leg press", "Leg press singola",
        "Leg extension", "Leg curl sdraiato", "Leg curl seduto",
        "Leg curl in piedi", "Affondi camminati", "Affondi indietro",
        "Bulgarian split squat", "Step-up", "Stacco rumeno",
        "Stacco a gambe tese", "Calf raise in piedi",
        "Calf pressa seduto", "Calf raise alla leg press",
        "Nordic hamstring curl", "Sissy squat", "Wall sit", "Estensione una gamba alla pressa orizzontale",
    ],
    "Glutei": [
        "Hip thrust bilanciere", "Hip thrust macchina", "Glute bridge",
        "Glute bridge a una gamba", "Kickback ai cavi",
        "Kickback macchina", "Abduttori macchina", "Abduzioni ai cavi",
        "Abduzioni con elastico", "Pull-through ai cavi",
        "Frog pump", "Donkey kick", "Fire hydrant",
        "Back extension focus glutei", "Adduttori macchina",
    ],
    "Addome": [
        "Crunch", "Crunch ai cavi", "Crunch macchina",
        "Reverse crunch", "Leg raise alla sbarra", "Leg raise alla panca",
        "Plank", "Side plank", "Ab wheel rollout",
        "Pallof press", "Russian twist", "Dead bug",
        "Hollow body hold", "Mountain climber", "Bicycle crunch", "Plank sui gomiti", "Crunch al cavo alto in ginocchio",
    ],
    "Polpacci e avambracci": [
        "Calf raise in piedi", "Calf raise seduto",
        "Wrist curl bilanciere", "Wrist curl inverso",
        "Farmer walk", "Pinch grip hold", "Dead hang",
    ],
    "Cardio": [
        "Tapis roulant", "Corsa", "Camminata in salita",
        "Cyclette", "Ellittica", "Vogatore", "Salto con la corda",
        "Air bike", "Stair climber", "Ski erg",
    ],
}


def ui_label(text, size=15, color=TEXT, height=dp(28), bold=False):
    return Label(
        text=text,
        color=color,
        font_size=sp(size),
        bold=bold,
        size_hint_y=None,
        height=height,
        halign="left",
        valign="middle",
        text_size=(None, None),
    )


def make_button(text, callback, color=ACCENT, height=dp(48), text_color=TEXT):
    button = Button(
        text=text,
        size_hint_y=None,
        height=height,
        background_normal="",
        background_down="",
        background_color=color,
        color=text_color,
        font_size=sp(14),
        bold=True,
    )
    button.bind(on_release=callback)
    return button


def make_input(hint, input_filter=None, text=""):
    return TextInput(
        hint_text=hint,
        text=text,
        multiline=False,
        input_filter=input_filter,
        size_hint_y=None,
        height=dp(46),
        padding=(dp(12), dp(12)),
        background_normal="",
        background_active="",
        background_color=CARD_ALT,
        foreground_color=TEXT,
        hint_text_color=MUTED,
        cursor_color=ACCENT,
        font_size=sp(15),
    )


class Card(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = dp(16)
        self.spacing = dp(10)
        with self.canvas.before:
            Color(*CARD)
            self.shape = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(18)])
        self.bind(pos=self._sync_shape, size=self._sync_shape)

    def _sync_shape(self, *_):
        self.shape.pos = self.pos
        self.shape.size = self.size


class DataStore:
    def __init__(self, path):
        self.path = path
        self.data = self._load()

    def _load(self):
        if not os.path.exists(self.path):
            return {
                "plans": [{
                    "id": "plan-1",
                    "name": "La mia scheda",
                    "days": [
                        {"id": "day-1", "name": "Giorno 1", "exercises": []},
                        {"id": "day-2", "name": "Giorno 2", "exercises": []},
                        {"id": "day-3", "name": "Giorno 3", "exercises": []},
                    ],
                    "selected_day_id": "day-1",
                }],
                "current_plan_id": "plan-1",
                "sessions": [],
                "body_weight": [],
                "profile": {"name": "", "sex": "", "age": ""},
                "settings": {
                    "workout_reminder": False,
                    "workout_time": "18:00",
                    "workout_interval_days": 1,
                    "weight_reminder": False,
                    "weight_interval_weeks": 1,
                    "workout_counter_reset_at": None,
                },
            }
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError) as error:
            raise RuntimeError("Impossibile leggere i dati salvati: {}".format(error)) from error
        required = ("plans", "current_plan_id", "sessions", "body_weight")
        if not isinstance(data, dict) or any(key not in data for key in required):
            raise RuntimeError("Il file dei dati salvati non ha un formato valido.")
        data.setdefault("settings", {})
        data.setdefault("profile", {})
        data["profile"] = {
            "name": str(data["profile"].get("name", "")),
            "sex": str(data["profile"].get("sex", "")),
            "age": str(data["profile"].get("age", "")),
        }
        data["settings"] = {
            "workout_reminder": bool(data["settings"].get("workout_reminder", False)),
            "workout_time": data["settings"].get("workout_time", "18:00"),
            "workout_interval_days": int(data["settings"].get("workout_interval_days", 1)),
            "weight_reminder": bool(data["settings"].get("weight_reminder", False)),
            "weight_interval_weeks": int(data["settings"].get("weight_interval_weeks", 1)),
            "workout_counter_reset_at": data["settings"].get("workout_counter_reset_at"),
        }
        if data["settings"]["workout_interval_days"] not in (1, 2, 3, 7):
            data["settings"]["workout_interval_days"] = 1
        for plan in data["plans"]:
            self.normalize_plan(plan)
        return data

    @staticmethod
    def normalize_plan(plan):
        days = plan.get("days")
        if not isinstance(days, list) or not days:
            exercises = plan.pop("exercises", [])
            days = [
                {"id": "day-1", "name": "Giorno 1", "exercises": exercises},
                {"id": "day-2", "name": "Giorno 2", "exercises": []},
                {"id": "day-3", "name": "Giorno 3", "exercises": []},
            ]
            plan["days"] = days
        for index, day in enumerate(days, start=1):
            day.setdefault("id", "day-{}".format(index))
            day.setdefault("name", "Giorno {}".format(index))
            day.setdefault("exercises", [])
            for exercise in day["exercises"]:
                exercise["notes"] = str(exercise.get("notes", ""))
        while len(days) < 2:
            index = len(days) + 1
            days.append({
                "id": "day-{}".format(index),
                "name": "Giorno {}".format(index),
                "exercises": [],
            })
        if plan.get("selected_day_id") not in {day["id"] for day in days}:
            plan["selected_day_id"] = days[0]["id"]

    def save(self):
        folder = os.path.dirname(self.path)
        os.makedirs(folder, exist_ok=True)
        temporary_path = self.path + ".tmp"
        try:
            with open(temporary_path, "w", encoding="utf-8") as file:
                json.dump(self.data, file, ensure_ascii=False, indent=2)
            os.replace(temporary_path, self.path)
        except OSError as error:
            raise RuntimeError("Impossibile salvare i dati: {}".format(error)) from error


class BaseScreen(Screen):
    def __init__(self, app, title, nav=True, **kwargs):
        screen_name = kwargs.get("name")
        super().__init__(**kwargs)
        self.app_ref = app
        self.root_box = BoxLayout(orientation="vertical", spacing=dp(6), padding=(dp(14), dp(8)))
        heading = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        title_label = ui_label(title, size=23, height=dp(44), bold=True)
        title_label.size_hint_x = 1
        heading.add_widget(title_label)
        settings_button = make_button(
            "←" if screen_name == "settings" else "⚙",
            lambda *_: self.app_ref.go("home" if screen_name == "settings" else "settings"),
            color=CARD_ALT,
            height=dp(38),
        )
        settings_button.size_hint_x = None
        settings_button.width = dp(42)
        heading.add_widget(settings_button)
        self.root_box.add_widget(heading)
        self.scroll = ScrollView(do_scroll_x=False, bar_width=dp(3))
        self.body = BoxLayout(orientation="vertical", spacing=dp(12), size_hint_y=None, padding=(0, dp(4)))
        self.body.bind(minimum_height=self.body.setter("height"))
        self.scroll.add_widget(self.body)
        self.root_box.add_widget(self.scroll)
        if nav:
            self.root_box.add_widget(self._navigation())
        self.add_widget(self.root_box)
        self.bind(on_pre_enter=self.refresh)

    def _navigation(self):
        bar = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
        for label, name in (
            ("Oggi", "home"), ("Scheda", "plans"),
            ("Analisi", "analytics"), ("Storico", "history"),
        ):
            bar.add_widget(make_button(label, lambda _button, target=name: self.app_ref.go(target),
                                       color=CARD_ALT, height=dp(46)))
        return bar

    def refresh(self, *_):
        self.body.clear_widgets()


class HomeScreen(BaseScreen):
    def __init__(self, app, **kwargs):
        super().__init__(app, "Allenamento", name="home", **kwargs)

    def refresh(self, *_):
        self.body.clear_widgets()
        plan = self.app_ref.current_plan()
        today = date.today().strftime("%d/%m/%Y")
        profile_name = self.app_ref.store.data["profile"]["name"].strip()
        greeting = "Ciao, {}".format(profile_name) if profile_name else "Ciao, atleta"
        self.body.add_widget(ui_label(greeting, 21, TEXT, height=dp(34), bold=True))
        self.body.add_widget(ui_label("Oggi · {}".format(today), 14, MUTED))
        day = self.app_ref.selected_day(plan)
        day_spinner = Spinner(
            text=day["name"],
            values=[item["name"] for item in plan["days"]],
            size_hint_y=None,
            height=dp(46),
            background_normal="",
            background_color=CARD_ALT,
            color=TEXT,
            font_size=sp(14),
        )
        day_spinner.bind(text=lambda _spinner, name: self.select_day(plan, name))
        self.body.add_widget(ui_label("Scegli il giorno da allenare", 13, MUTED))
        self.body.add_widget(day_spinner)
        welcome = Card(orientation="vertical", size_hint_y=None, height=dp(170))
        welcome.add_widget(ui_label("Pronto a dare il meglio?", 20, TEXT, bold=True))
        welcome.add_widget(ui_label("{} · {}".format(plan["name"], day["name"]), 14, MUTED))
        welcome.add_widget(make_button("INIZIA ALLENAMENTO", lambda *_: self.app_ref.start_workout(day["id"]),
                                       color=ACCENT, height=dp(54)))
        self.body.add_widget(welcome)

        stats = self.app_ref.quick_stats()
        summary = Card(orientation="vertical", size_hint_y=None, height=dp(118))
        summary.add_widget(ui_label("IL TUO PERCORSO", 12, MUTED, bold=True))
        summary.add_widget(ui_label("{} allenamenti completati".format(stats["workouts"]), 17, TEXT, bold=True))
        summary.add_widget(ui_label("Ultimo allenamento: {}".format(stats["last"]), 13, MUTED))
        self.body.add_widget(summary)

        self.body.add_widget(ui_label("Esercizi · {}".format(day["name"]), 18, TEXT, bold=True))
        if day["exercises"]:
            for entry in day["exercises"][:5]:
                self.body.add_widget(ui_label(
                    "{}  ·  {} serie".format(entry["name"], entry.get("sets", 3)), 14, MUTED
                ))
            if len(day["exercises"]) > 5:
                self.body.add_widget(ui_label("+ altri {} esercizi".format(len(day["exercises"]) - 5), 13, MUTED))
        else:
            self.body.add_widget(ui_label("Aggiungi esercizi a questo giorno dalla pagina Scheda.", 14, MUTED))

    def select_day(self, plan, day_name):
        day = next((item for item in plan["days"] if item["name"] == day_name), None)
        if day:
            plan["selected_day_id"] = day["id"]
            self.app_ref.store.save()
            self.refresh()


class PlansScreen(BaseScreen):
    def __init__(self, app, **kwargs):
        super().__init__(app, "Scheda", name="plans", **kwargs)

    def refresh(self, *_):
        self.body.clear_widgets()
        self.body.add_widget(ui_label(
            "Crea fino a 5 schede e seleziona quella che stai seguendo.", 14, MUTED, height=dp(44)
        ))
        for plan in self.app_ref.store.data["plans"]:
            day_count = len(plan["days"])
            exercise_count = sum(len(day["exercises"]) for day in plan["days"])
            is_current = plan["id"] == self.app_ref.store.data["current_plan_id"]
            card = Card(orientation="vertical", size_hint_y=None, height=dp(168))
            card.add_widget(ui_label(
                ("✓  " if is_current else "") + plan["name"],
                18, MINT if is_current else TEXT, bold=True
            ))
            card.add_widget(ui_label(
                "{} giorni · {} esercizi".format(day_count, exercise_count), 13, MUTED
            ))
            actions = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
            if not is_current:
                actions.add_widget(make_button(
                    "Attiva", lambda _button, plan_id=plan["id"]: self.select_plan(plan_id),
                    color=CARD_ALT, height=dp(42)
                ))
            actions.add_widget(make_button(
                "Modifica", lambda _button, selected=plan: self.edit_plan(selected),
                color=ACCENT, height=dp(42)
            ))
            actions.add_widget(make_button(
                "Elimina", lambda _button, selected=plan: self.confirm_delete_plan(selected),
                color=(0.45, 0.18, 0.22, 1), height=dp(42)
            ))
            card.add_widget(actions)
            self.body.add_widget(card)
        if len(self.app_ref.store.data["plans"]) < 5:
            self.body.add_widget(make_button("＋  Crea una nuova scheda", self.create_plan, height=dp(50)))

    def select_plan(self, plan_id):
        self.app_ref.store.data["current_plan_id"] = plan_id
        self.app_ref.store.save()
        self.refresh()

    def confirm_delete_plan(self, plan):
        content = BoxLayout(orientation="vertical", spacing=dp(12), padding=dp(14))
        content.add_widget(ui_label(
            "La scheda e i suoi giorni verranno eliminati. Gli allenamenti già salvati resteranno nello storico.",
            13, TEXT, height=dp(64)
        ))
        popup = Popup(title="Eliminare questa scheda?", content=content, size_hint=(0.9, 0.34))
        actions = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        actions.add_widget(make_button(
            "Annulla", lambda *_: popup.dismiss(), color=CARD_ALT, height=dp(44)
        ))

        def delete(_button):
            plans = self.app_ref.store.data["plans"]
            if len(plans) <= 1:
                popup.dismiss()
                self.app_ref.message("Mantieni almeno una scheda. Puoi crearne un'altra prima di eliminare questa.")
                return
            plans.remove(plan)
            if self.app_ref.store.data["current_plan_id"] == plan["id"]:
                self.app_ref.store.data["current_plan_id"] = plans[0]["id"]
            self.app_ref.store.save()
            popup.dismiss()
            self.refresh()

        actions.add_widget(make_button(
            "Elimina", delete, color=(0.45, 0.18, 0.22, 1), height=dp(44)
        ))
        content.add_widget(actions)
        popup.open()

    def create_plan(self, *_):
        plans = self.app_ref.store.data["plans"]
        if len(plans) >= 5:
            return
        plan = {
            "id": "plan-{}".format(datetime.now().strftime("%Y%m%d%H%M%S%f")),
            "name": "Nuova scheda {}".format(len(plans) + 1),
            "days": [
                {"id": "day-1", "name": "Giorno 1", "exercises": []},
                {"id": "day-2", "name": "Giorno 2", "exercises": []},
                {"id": "day-3", "name": "Giorno 3", "exercises": []},
            ],
            "selected_day_id": "day-1",
        }
        plans.append(plan)
        self.app_ref.store.data["current_plan_id"] = plan["id"]
        self.app_ref.store.save()
        self.edit_plan(plan)
        self.refresh()

    def edit_plan(self, plan):
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(14))
        name_input = make_input("Nome della scheda", text=plan["name"])
        content.add_widget(name_input)
        day_spinner = Spinner(
            text=self.app_ref.selected_day(plan)["name"],
            values=[day["name"] for day in plan["days"]],
            size_hint_y=None,
            height=dp(44),
            background_normal="",
            background_color=CARD_ALT,
            color=TEXT,
            font_size=sp(14),
        )
        day_actions = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        day_actions.add_widget(day_spinner)
        day_name_input = make_input("Nome del giorno", text=self.app_ref.selected_day(plan)["name"])
        rename_row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        rename_row.add_widget(day_name_input)
        exercise_list = BoxLayout(orientation="vertical", spacing=dp(6), size_hint_y=None)
        exercise_list.bind(minimum_height=exercise_list.setter("height"))
        list_scroll = ScrollView(do_scroll_x=False, size_hint_y=1)
        list_scroll.add_widget(exercise_list)
        popup = Popup(title="Modifica scheda", content=content, size_hint=(0.94, 0.9))

        def selected_day():
            return self.app_ref.selected_day(plan)

        def redraw_exercises():
            exercise_list.clear_widgets()
            for index, exercise in enumerate(selected_day()["exercises"]):
                item = BoxLayout(
                    orientation="vertical", size_hint_y=None, height=dp(128), spacing=dp(4)
                )
                name_label = ui_label(exercise["name"], 13, TEXT, height=dp(32), bold=True)
                name_label.bind(
                    width=lambda label, width: setattr(label, "text_size", (width, None))
                )
                item.add_widget(name_label)
                row = BoxLayout(size_hint_y=None, height=dp(34), spacing=dp(6))
                minus = make_button(
                    "−", lambda _button, i=index: change_sets(i, -1),
                    color=CARD_ALT, height=dp(34)
                )
                minus.size_hint_x, minus.width = None, dp(34)
                row.add_widget(minus)
                set_count = ui_label(str(exercise.get("sets", 3)), 12, MUTED, height=dp(34))
                set_count.size_hint_x = None
                set_count.width = dp(24)
                row.add_widget(set_count)
                plus = make_button(
                    "+", lambda _button, i=index: change_sets(i, 1),
                    color=CARD_ALT, height=dp(34)
                )
                plus.size_hint_x, plus.width = None, dp(34)
                row.add_widget(plus)
                remove = make_button(
                    "Rimuovi", lambda _button, i=index: remove_exercise(i),
                    color=(0.45, 0.18, 0.22, 1), height=dp(34)
                )
                remove.size_hint_x, remove.width = None, dp(74)
                row.add_widget(remove)
                item.add_widget(row)
                notes = TextInput(
                    hint_text="Note per questo esercizio",
                    text=exercise.get("notes", ""),
                    multiline=True,
                    size_hint_y=None,
                    height=dp(52),
                    padding=(dp(10), dp(8)),
                    background_normal="",
                    background_active="",
                    background_color=CARD_ALT,
                    foreground_color=TEXT,
                    hint_text_color=MUTED,
                    cursor_color=ACCENT,
                    font_size=sp(13),
                )
                notes.bind(text=lambda _input, value, entry=exercise: entry.__setitem__("notes", value))
                item.add_widget(notes)
                exercise_list.add_widget(item)

        def change_sets(index, amount):
            exercise = selected_day()["exercises"][index]
            exercise["sets"] = max(1, min(12, exercise.get("sets", 3) + amount))
            redraw_exercises()

        def remove_exercise(index):
            del selected_day()["exercises"][index]
            redraw_exercises()

        def add_exercise(_button):
            self.show_exercise_picker(lambda exercise: append_exercise(exercise))

        def append_exercise(exercise):
            exercises = selected_day()["exercises"]
            if not any(item["name"] == exercise for item in exercises):
                exercises.append({"name": exercise, "sets": 3, "notes": ""})
                redraw_exercises()

        def select_day(_spinner, day_name):
            day = next((item for item in plan["days"] if item["name"] == day_name), None)
            if day:
                plan["selected_day_id"] = day["id"]
                day_name_input.text = day["name"]
                redraw_exercises()

        def rename_day(_button):
            new_name = day_name_input.text.strip()
            day = selected_day()
            if not new_name:
                self.app_ref.message("Inserisci un nome per il giorno.")
                return
            if any(
                item["id"] != day["id"] and item["name"].casefold() == new_name.casefold()
                for item in plan["days"]
            ):
                self.app_ref.message("Questo nome è già usato in un altro giorno della scheda.")
                return
            day["name"] = new_name
            day_spinner.values = [item["name"] for item in plan["days"]]
            day_spinner.text = new_name
            self.app_ref.store.save()

        def add_day(_button):
            if len(plan["days"]) >= 7:
                self.app_ref.message("Una scheda può contenere al massimo 7 giorni.")
                return
            used_names = {day["name"] for day in plan["days"]}
            index = 1
            while "Giorno {}".format(index) in used_names:
                index += 1
            day = {
                "id": "day-{}".format(datetime.now().strftime("%Y%m%d%H%M%S%f")),
                "name": "Giorno {}".format(index),
                "exercises": [],
            }
            plan["days"].append(day)
            plan["selected_day_id"] = day["id"]
            day_spinner.values = [item["name"] for item in plan["days"]]
            day_spinner.text = day["name"]
            day_name_input.text = day["name"]
            redraw_exercises()

        def remove_day(_button):
            if len(plan["days"]) <= 2:
                self.app_ref.message("Ogni scheda deve avere almeno due giorni.")
                return
            day = selected_day()
            plan["days"].remove(day)
            plan["selected_day_id"] = plan["days"][0]["id"]
            day_spinner.values = [item["name"] for item in plan["days"]]
            day_spinner.text = plan["days"][0]["name"]
            day_name_input.text = plan["days"][0]["name"]
            redraw_exercises()

        day_spinner.bind(text=select_day)
        rename_row.add_widget(make_button("Rinomina", rename_day, color=ACCENT, height=dp(42)))
        day_actions.add_widget(make_button("＋ Giorno", add_day, color=CARD_ALT, height=dp(42)))
        day_actions.add_widget(make_button("−", remove_day, color=(0.45, 0.18, 0.22, 1),
                                           height=dp(42)))
        content.add_widget(day_actions)
        content.add_widget(rename_row)
        content.add_widget(ui_label("Esercizi del giorno selezionato", 12, MUTED))
        content.add_widget(list_scroll)

        actions = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        actions.add_widget(make_button("＋ Aggiungi esercizio", add_exercise, color=CARD_ALT, height=dp(44)))

        def save_plan(_button):
            name = name_input.text.strip()
            if name:
                plan["name"] = name
            self.app_ref.store.save()
            popup.dismiss()
            self.refresh()

        actions.add_widget(make_button("Salva", save_plan, height=dp(44)))
        content.add_widget(actions)
        redraw_exercises()
        popup.open()

    def show_exercise_picker(self, on_select):
        content = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(12))
        search = make_input("Cerca un esercizio")
        content.add_widget(search)
        matches = BoxLayout(orientation="vertical", spacing=dp(4), size_hint_y=None)
        matches.bind(minimum_height=matches.setter("height"))
        list_scroll = ScrollView(do_scroll_x=False)
        list_scroll.add_widget(matches)
        content.add_widget(list_scroll)
        popup = Popup(title="Catalogo esercizi", content=content, size_hint=(0.92, 0.88))
        all_names = [name for names in EXERCISES.values() for name in names]

        def update_matches(*_):
            matches.clear_widgets()
            query = search.text.casefold().strip()
            results = [name for name in all_names if query in name.casefold()]
            for name in results:
                button = make_button(name, lambda _button, value=name: choose(value),
                                     color=CARD_ALT, height=dp(42))
                matches.add_widget(button)
            if not results:
                matches.add_widget(ui_label("Nessun esercizio trovato", 13, MUTED))

        def choose(name):
            on_select(name)
            popup.dismiss()

        search.bind(text=update_matches)
        update_matches()
        popup.open()


class WorkoutScreen(BaseScreen):
    def __init__(self, app, **kwargs):
        super().__init__(app, "Allenamento in corso", name="workout", nav=False, **kwargs)
        self.entries = []

    def refresh(self, *_):
        self.body.clear_widgets()
        self.entries = []
        workout = self.app_ref.active_workout
        if not workout:
            self.body.add_widget(ui_label("Nessun allenamento attivo.", 14, MUTED))
            return
        self.body.add_widget(ui_label(
            "{} · {}  ·  {}".format(
                workout["plan_name"], workout["day_name"], datetime.now().strftime("%d/%m/%Y")
            ),
            14, MUTED
        ))
        if not workout["exercises"]:
            self.body.add_widget(ui_label(
                "Questa giornata non ha ancora esercizi. Aggiungili dalla sezione Scheda.",
                14, MUTED, height=dp(54)
            ))
        else:
            index = min(workout.get("exercise_index", 0), len(workout["exercises"]) - 1)
            workout["exercise_index"] = index
            self.body.add_widget(ui_label(
                "ESERCIZIO {} DI {}".format(index + 1, len(workout["exercises"])),
                13, MINT, height=dp(32), bold=True
            ))
            self.add_exercise_form(workout["exercises"][index])
            if index == len(workout["exercises"]) - 1:
                self.body.add_widget(make_button(
                    "TERMINA E SALVA ALLENAMENTO", self.finish_workout,
                    color=MINT, text_color=BG, height=dp(54)
                ))
            else:
                self.body.add_widget(make_button(
                    "PROSSIMO ESERCIZIO", self.next_exercise,
                    color=ACCENT, height=dp(54)
                ))
            previous = make_button(
                "← ESERCIZIO PRECEDENTE", self.previous_exercise,
                color=CARD_ALT, height=dp(46)
            )
            previous.disabled = index == 0
            self.body.add_widget(previous)
        self.body.add_widget(make_button("Annulla", self.cancel_workout, color=(0.25, 0.29, 0.37, 1)))

    def add_exercise_form(self, exercise):
        notes = exercise.get("notes", "").strip()
        card_height = 130 + len(exercise["sets"]) * 52 + (50 if notes else 0)
        card = Card(orientation="vertical", size_hint_y=None, height=dp(card_height))
        name_label = ui_label(exercise["name"], 16, TEXT, height=dp(44), bold=True)
        name_label.bind(width=lambda label, width: setattr(label, "text_size", (width, None)))
        card.add_widget(name_label)
        if notes:
            notes_label = ui_label("Note: {}".format(notes), 13, MUTED, height=dp(50))
            notes_label.bind(width=lambda label, width: setattr(label, "text_size", (width, None)))
            card.add_widget(notes_label)
        card.add_widget(ui_label("Serie     Ripetizioni          Peso (kg)", 11, MUTED))
        fields = []
        for index, set_data in enumerate(exercise["sets"], start=1):
            row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
            set_number = ui_label(str(index), 13, MUTED, height=dp(42))
            set_number.size_hint_x = None
            set_number.width = dp(44)
            row.add_widget(set_number)
            reps = make_input("Reps", input_filter="int", text=set_data.get("reps", ""))
            weight = make_input("kg", input_filter="float", text=set_data.get("weight", ""))
            row.add_widget(reps)
            row.add_widget(weight)
            card.add_widget(row)
            fields.append((reps, weight))
        self.body.add_widget(card)
        self.entries = [(exercise, fields)]

    def save_current_exercise(self, require_complete):
        if not self.entries:
            return True
        exercise, fields = self.entries[0]
        saved_sets = []
        try:
            for reps_input, weight_input in fields:
                reps_text = reps_input.text.strip()
                weight_text = weight_input.text.strip().replace(",", ".")
                if require_complete and (not reps_text or not weight_text):
                    raise ValueError("Completa ripetizioni e peso per ogni serie.")
                if require_complete:
                    reps = int(reps_text)
                    weight = float(weight_text)
                    if reps < 1 or weight < 0:
                        raise ValueError("Inserisci ripetizioni positive e un peso non negativo.")
                saved_sets.append({"reps": reps_text, "weight": weight_text})
        except ValueError as error:
            self.app_ref.message(str(error))
            return False
        exercise["sets"] = saved_sets
        return True

    def next_exercise(self, *_):
        if not self.save_current_exercise(require_complete=True):
            return
        workout = self.app_ref.active_workout
        workout["exercise_index"] += 1
        self.refresh()

    def previous_exercise(self, *_):
        if not self.save_current_exercise(require_complete=False):
            return
        workout = self.app_ref.active_workout
        workout["exercise_index"] = max(0, workout["exercise_index"] - 1)
        self.refresh()

    def finish_workout(self, *_):
        workout = self.app_ref.active_workout
        if not workout or not workout["exercises"]:
            self.app_ref.message("Aggiungi almeno un esercizio prima di salvare.")
            return
        if workout["exercise_index"] < len(workout["exercises"]) - 1:
            self.app_ref.message("Completa prima tutti gli esercizi.")
            return
        if not self.save_current_exercise(require_complete=True):
            return
        logged_exercises = []
        try:
            for exercise in workout["exercises"]:
                sets = []
                for set_data in exercise["sets"]:
                    reps_text = str(set_data.get("reps", "")).strip()
                    weight_text = str(set_data.get("weight", "")).strip().replace(",", ".")
                    if not reps_text or not weight_text:
                        raise ValueError("Completa ripetizioni e peso per ogni serie.")
                    reps = int(reps_text)
                    weight = float(weight_text)
                    if reps < 1 or weight < 0:
                        raise ValueError("Inserisci ripetizioni positive e un peso non negativo.")
                    sets.append({"reps": reps, "weight": weight})
                logged_exercises.append({"name": exercise["name"], "sets": sets})
        except ValueError as error:
            self.app_ref.message(str(error))
            return
        completed_at = datetime.now().isoformat(timespec="seconds")
        self.app_ref.store.data["sessions"].append({
            "date": date.today().isoformat(),
            "completed_at": completed_at,
            "plan_id": workout["plan_id"],
            "plan_name": workout["plan_name"],
            "day_id": workout["day_id"],
            "day_name": workout["day_name"],
            "exercises": logged_exercises,
        })
        self.app_ref.store.save()
        self.app_ref.active_workout = None
        self.app_ref.message("Allenamento salvato. Ottimo lavoro!")
        self.app_ref.go("home")

    def cancel_workout(self, *_):
        self.app_ref.active_workout = None
        self.app_ref.go("home")


class HistoryScreen(BaseScreen):
    def __init__(self, app, **kwargs):
        super().__init__(app, "Storico allenamenti", name="history", **kwargs)

    def refresh(self, *_):
        self.body.clear_widgets()

        def completed_datetime(session):
            try:
                timestamp = session.get("completed_at")
                if not timestamp:
                    raise ValueError("Orario non registrato")
                completed = datetime.fromisoformat(timestamp)
            except (TypeError, ValueError):
                completed = datetime.combine(
                    date.fromisoformat(session["date"]), datetime.min.time()
                )
            if completed.tzinfo is not None:
                completed = completed.astimezone().replace(tzinfo=None)
            return completed

        cutoff = datetime.now() - timedelta(days=30)
        recent_sessions = [
            session for session in self.app_ref.store.data["sessions"]
            if completed_datetime(session) >= cutoff
        ]
        recent_sessions.sort(key=completed_datetime, reverse=True)
        self.body.add_widget(ui_label("Sessioni degli ultimi 30 giorni", 13, MUTED))
        if not recent_sessions:
            self.body.add_widget(ui_label(
                "Non ci sono allenamenti registrati nell'ultimo mese.", 14, MUTED
            ))
            return

        for session in recent_sessions:
            completed_at = session.get("completed_at")
            if completed_at:
                try:
                    completed = completed_datetime(session)
                    date_label = completed.strftime("%d/%m/%Y · %H:%M")
                except ValueError:
                    date_label = "{} · orario non disponibile".format(
                        datetime.fromisoformat(session["date"]).strftime("%d/%m/%Y")
                    )
            else:
                date_label = "{} · orario non disponibile".format(
                    datetime.fromisoformat(session["date"]).strftime("%d/%m/%Y")
                )
            exercises = session.get("exercises", [])
            card = Card(
                orientation="vertical",
                size_hint_y=None,
                height=dp(86),
            )
            day_name = session.get("day_name", "Allenamento")
            details = BoxLayout(
                orientation="vertical",
                spacing=dp(4),
                size_hint_y=None,
                height=0,
            )
            details.add_widget(ui_label(
                "{} · {}".format(session.get("plan_name", "Scheda"), day_name),
                13, MUTED,
            ))
            for exercise in exercises:
                details.add_widget(ui_label(exercise.get("name", "Esercizio"), 13, TEXT, bold=True))
                for index, set_data in enumerate(exercise.get("sets", []), start=1):
                    details.add_widget(ui_label(
                        "Serie {} · {} rip · {:.1f} kg".format(
                            index,
                            set_data.get("reps", 0),
                            set_data.get("weight", 0),
                        ),
                        12, MUTED, height=dp(22),
                    ))

            def toggle_details(_button, detail_box=details, parent_card=card):
                is_open = detail_box.height == 0
                detail_box.height = detail_box.minimum_height if is_open else 0
                parent_card.height = dp(86) + detail_box.height

            card.add_widget(make_button(
                "{}     {}".format(date_label, day_name),
                toggle_details,
                color=CARD_ALT,
                height=dp(44),
            ))
            card.add_widget(details)
            self.body.add_widget(card)


class LineChart(Widget):
    def __init__(self, points=None, **kwargs):
        super().__init__(**kwargs)
        self.points = points or []
        self.bind(pos=self.draw, size=self.draw)
        self.draw()

    def set_points(self, points):
        self.points = points
        self.draw()

    def draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*CARD_ALT)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
            left, right = self.x + dp(22), self.right - dp(14)
            bottom, top = self.y + dp(18), self.top - dp(18)
            values = [point[1] for point in self.points]
            low = min(values) if values else 0
            high = max(values) if values else 1
            if high == low:
                low = max(0, low - 1)
                high += 1
            margin = max((high - low) * 0.18, 0.5)
            low -= margin
            high += margin
            for index in range(4):
                y = bottom + (top - bottom) * index / 3
                Color(0.26, 0.31, 0.40, 0.7)
                Line(points=[left, y, right, y], width=0.7)
            if len(self.points) >= 2:
                first = datetime.fromisoformat(self.points[0][0]).date()
                last = datetime.fromisoformat(self.points[-1][0]).date()
                span = max((last - first).days, 1)
                coords = []
                for day, value in self.points:
                    x = left + (right - left) * (datetime.fromisoformat(day).date() - first).days / span
                    y = bottom + (top - bottom) * (value - low) / (high - low)
                    coords.extend((x, y))
                Color(*ACCENT)
                Line(points=coords, width=dp(2.4), cap="round", joint="round")
                for index in range(0, len(coords), 2):
                    Color(*MINT)
                    Ellipse(pos=(coords[index] - dp(4), coords[index + 1] - dp(4)),
                            size=(dp(8), dp(8)))
            elif len(self.points) == 1:
                Color(*MINT)
                Ellipse(pos=(self.center_x - dp(4), self.center_y - dp(4)),
                        size=(dp(8), dp(8)))


class AnalyticsScreen(BaseScreen):
    def __init__(self, app, **kwargs):
        super().__init__(app, "Analisi crescita", name="analytics", **kwargs)

    def refresh(self, *_):
        self.body.clear_widgets()
        self.body.add_widget(ui_label(
            "Scheda attiva: {}".format(self.app_ref.current_plan()["name"]), 13, MUTED
        ))
        names = sorted({
            exercise["name"]
            for session in self.app_ref.store.data["sessions"]
            if session.get("plan_id") == self.app_ref.store.data["current_plan_id"]
            for exercise in session["exercises"]
        })
        self.body.add_widget(ui_label("I tuoi record", 18, TEXT, bold=True))
        bests = self.app_ref.exercise_bests()
        if not bests:
            self.body.add_widget(ui_label("Completa un allenamento per vedere i tuoi progressi.", 14, MUTED))
        else:
            for name, weight in sorted(bests.items(), key=lambda item: (-item[1], item[0])):
                self.body.add_widget(ui_label("{}  ·  {:.1f} kg".format(name, weight), 14, MUTED))

        self.body.add_widget(ui_label("Progressi per esercizio · ultimi 60 giorni", 17, TEXT, bold=True))
        self.exercise_spinner = Spinner(
            text=names[0] if names else "Nessun esercizio registrato",
            values=names,
            size_hint_y=None,
            height=dp(46),
            background_normal="",
            background_color=CARD_ALT,
            color=TEXT,
            font_size=sp(14),
        )
        self.exercise_spinner.bind(text=self.update_exercise_chart)
        self.body.add_widget(self.exercise_spinner)
        self.exercise_chart = LineChart(size_hint_y=None, height=dp(200))
        self.body.add_widget(self.exercise_chart)
        self.exercise_summary = ui_label("", 13, MUTED, height=dp(42))
        self.body.add_widget(self.exercise_summary)
        self.update_exercise_chart()

        self.body.add_widget(ui_label("Peso corporeo", 18, TEXT, bold=True))
        self.body.add_widget(ui_label(
            "Registra il peso una volta a settimana per seguire l'andamento.", 13, MUTED, height=dp(38)
        ))
        weight_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.weight_input = make_input("Peso in kg", input_filter="float")
        weight_row.add_widget(self.weight_input)
        weight_row.add_widget(make_button("Registra", self.save_body_weight, height=dp(46)))
        self.body.add_widget(weight_row)
        body_points = self.app_ref.recent_body_weight()
        self.body_weight_chart = LineChart(body_points, size_hint_y=None, height=dp(200))
        self.body.add_widget(self.body_weight_chart)
        if body_points:
            self.body.add_widget(ui_label(
                "Ultima registrazione: {} · {:.1f} kg".format(body_points[-1][0], body_points[-1][1]),
                13, MUTED
            ))
        else:
            self.body.add_widget(ui_label("Nessun peso registrato.", 13, MUTED))

    def update_exercise_chart(self, *_):
        if not hasattr(self, "exercise_chart"):
            return
        name = self.exercise_spinner.text
        points = self.app_ref.recent_exercise_progress(name)
        self.exercise_chart.set_points(points)
        if points:
            self.exercise_summary.text = (
                "Miglior carico nel periodo: {:.1f} kg  ·  {} sessioni".format(
                    max(value for _, value in points), len(points)
                )
            )
        else:
            self.exercise_summary.text = "Nessun dato negli ultimi 60 giorni per questo esercizio."

    def save_body_weight(self, *_):
        value_text = self.weight_input.text.strip().replace(",", ".")
        try:
            weight = float(value_text)
            if weight <= 0 or weight > 500:
                raise ValueError
        except ValueError:
            self.app_ref.message("Inserisci un peso corporeo valido in kg.")
            return
        today = date.today().isoformat()
        records = self.app_ref.store.data["body_weight"]
        current_week = date.today().isocalendar()[:2]
        existing = next((
            item for item in records
            if date.fromisoformat(item["date"]).isocalendar()[:2] == current_week
        ), None)
        if existing:
            existing["date"] = today
            existing["weight"] = weight
        else:
            records.append({"date": today, "weight": weight})
        self.app_ref.store.save()
        self.weight_input.text = ""
        self.refresh()


class SettingsScreen(BaseScreen):
    def __init__(self, app, **kwargs):
        super().__init__(app, "Impostazioni", name="settings", **kwargs)

    def refresh(self, *_):
        self.body.clear_widgets()
        profile = self.app_ref.store.data["profile"]
        profile_card = Card(orientation="vertical", size_hint_y=None, height=dp(340))
        profile_card.add_widget(ui_label("Profilo utente", 17, TEXT, bold=True))
        profile_card.add_widget(ui_label("Le tue informazioni personali.", 12, MUTED))
        self.profile_name = make_input("Nome", text=profile["name"])
        profile_card.add_widget(self.profile_name)
        self.profile_sex = Spinner(
            text=profile["sex"] or "Sesso (facoltativo)",
            values=("Donna", "Uomo", "Altro", "Preferisco non specificare"),
            size_hint_y=None,
            height=dp(44),
            background_normal="",
            background_color=CARD_ALT,
            color=TEXT,
            font_size=sp(14),
        )
        profile_card.add_widget(self.profile_sex)
        self.profile_age = make_input("Età (facoltativa)", input_filter="int", text=profile["age"])
        profile_card.add_widget(self.profile_age)
        profile_card.add_widget(make_button(
            "Salva profilo", self.save_profile, color=ACCENT, height=dp(44)
        ))
        self.body.add_widget(profile_card)

        settings = self.app_ref.store.data["settings"]
        workout_card = Card(orientation="vertical", size_hint_y=None, height=dp(260))
        workout_card.add_widget(ui_label("Promemoria allenamento", 17, TEXT, bold=True))
        workout_card.add_widget(ui_label(
            "Un piccolo incoraggiamento per la tua prossima sessione.", 12, MUTED
        ))
        workout_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        workout_row.add_widget(ui_label("Attiva promemoria", 14, TEXT))
        workout_switch = Switch(active=settings["workout_reminder"], size_hint_x=None, width=dp(60))
        workout_switch.bind(active=lambda _switch, value: self.update_setting("workout_reminder", value))
        workout_row.add_widget(workout_switch)
        workout_card.add_widget(workout_row)
        workout_card.add_widget(self.time_picker(
            "Orario", "workout_time", settings["workout_time"]
        ))
        workout_interval_row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        workout_interval_row.add_widget(ui_label("Frequenza", 14, TEXT))
        interval_labels = {
            1: "Ogni giorno",
            2: "Ogni 2 giorni",
            3: "Ogni 3 giorni",
            7: "Ogni settimana",
        }
        workout_interval = Spinner(
            text=interval_labels[settings["workout_interval_days"]],
            values=tuple(interval_labels.values()),
            size_hint_x=None,
            width=dp(142),
            background_normal="",
            background_color=CARD_ALT,
            color=TEXT,
        )
        workout_interval.bind(text=lambda _spinner, value: self.update_setting(
            "workout_interval_days",
            next(days for days, label in interval_labels.items() if label == value),
        ))
        workout_interval_row.add_widget(workout_interval)
        workout_card.add_widget(workout_interval_row)
        self.body.add_widget(workout_card)

        weight_card = Card(orientation="vertical", size_hint_y=None, height=dp(205))
        weight_card.add_widget(ui_label("Promemoria peso corporeo", 17, TEXT, bold=True))
        weight_card.add_widget(ui_label(
            "Ricordati di aggiornare il peso per il grafico.", 12, MUTED
        ))
        weight_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        weight_row.add_widget(ui_label("Attiva promemoria", 14, TEXT))
        weight_switch = Switch(active=settings["weight_reminder"], size_hint_x=None, width=dp(60))
        weight_switch.bind(active=lambda _switch, value: self.update_setting("weight_reminder", value))
        weight_row.add_widget(weight_switch)
        weight_card.add_widget(weight_row)
        interval_row = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        interval_row.add_widget(ui_label("Frequenza", 14, TEXT))
        interval = Spinner(
            text=str(settings["weight_interval_weeks"]),
            values=("1", "2", "3"),
            size_hint_x=None,
            width=dp(86),
            background_normal="",
            background_color=CARD_ALT,
            color=TEXT,
        )
        interval.bind(text=lambda _spinner, value: self.update_setting(
            "weight_interval_weeks", int(value)
        ))
        interval_row.add_widget(interval)
        interval_row.add_widget(ui_label("settimane", 13, MUTED))
        weight_card.add_widget(interval_row)
        self.body.add_widget(weight_card)
        self.body.add_widget(ui_label(
            "Le preferenze vengono salvate sul dispositivo. La consegna programmata "
            "quando l'app è chiusa richiede l'integrazione dei promemoria nativi "
            "e i relativi permessi nella build mobile.",
            12, MUTED, height=dp(74)
        ))
        cache_card = Card(orientation="vertical", size_hint_y=None, height=dp(170))
        cache_card.add_widget(ui_label("Cache dell'app", 17, TEXT, bold=True))
        cache_card.add_widget(ui_label(
            "Svuota i dati temporanei senza eliminare schede, profilo o allenamenti.",
            12, MUTED, height=dp(40)
        ))
        cache_card.add_widget(make_button(
            "Svuota cache", self.confirm_clear_cache, color=CARD_ALT
        ))
        self.body.add_widget(cache_card)
        self.body.add_widget(ui_label("Contatore allenamenti completati", 17, TEXT, bold=True))
        self.body.add_widget(ui_label(
            "Azzera solo il conteggio mostrato nella schermata principale. "
            "Cronologia, record e grafici non verranno cancellati.",
            12, MUTED, height=dp(48)
        ))
        self.body.add_widget(make_button(
            "Azzera allenamenti completati",
            self.confirm_reset_workout_counter,
            color=(0.45, 0.18, 0.22, 1),
        ))

    def confirm_clear_cache(self, *_):
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        content.add_widget(ui_label(
            "Verranno rimossi solo i dati temporanei dell'app. Schede, profilo, "
            "sessioni e peso corporeo resteranno intatti.",
            13, TEXT, height=dp(64)
        ))
        popup = Popup(title="Svuotare la cache?", content=content, size_hint=(0.88, 0.4))
        actions = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        actions.add_widget(make_button(
            "Annulla", lambda *_: popup.dismiss(), color=CARD_ALT, height=dp(44)
        ))

        def clear_cache(_button):
            for category in tuple(Cache._objects):
                Cache.remove(category)
            popup.dismiss()
            self.app_ref.message("Cache svuotata. I tuoi dati sono intatti.")

        actions.add_widget(make_button(
            "Svuota", clear_cache, color=(0.45, 0.18, 0.22, 1), height=dp(44)
        ))
        content.add_widget(actions)
        popup.open()

    def time_picker(self, label, setting_key, selected):
        row = BoxLayout(size_hint_y=None, height=dp(42), spacing=dp(8))
        row.add_widget(ui_label(label, 14, TEXT))
        times = tuple(
            "{:02d}:{:02d}".format(hour, minute)
            for hour in range(24)
            for minute in (0, 30)
        )
        picker = Spinner(
            text=selected,
            values=times,
            size_hint_x=None,
            width=dp(96),
            background_normal="",
            background_color=CARD_ALT,
            color=TEXT,
        )
        picker.bind(text=lambda _spinner, value: self.update_setting(setting_key, value))
        row.add_widget(picker)
        return row

    def update_setting(self, key, value):
        self.app_ref.store.data["settings"][key] = value
        self.app_ref.store.save()

    def confirm_reset_workout_counter(self, *_):
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        content.add_widget(ui_label(
            "Il conteggio ripartirà da zero. Le sessioni salvate, i record e i grafici resteranno intatti.",
            13, TEXT, height=dp(60)
        ))
        popup = Popup(title="Azzera il contatore?", content=content, size_hint=(0.88, 0.36))
        actions = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(8))
        actions.add_widget(make_button(
            "Annulla", lambda *_: popup.dismiss(), color=CARD_ALT, height=dp(44)
        ))

        def reset(_button):
            self.app_ref.store.data["settings"]["workout_counter_reset_at"] = (
                datetime.now().isoformat(timespec="seconds")
            )
            self.app_ref.store.save()
            popup.dismiss()
            self.app_ref.message("Contatore azzerato. La cronologia è stata conservata.")

        actions.add_widget(make_button("Azzera", reset, color=(0.45, 0.18, 0.22, 1), height=dp(44)))
        content.add_widget(actions)
        popup.open()

    def save_profile(self, *_):
        name = self.profile_name.text.strip()
        age_text = self.profile_age.text.strip()
        if age_text and (not age_text.isdigit() or not 1 <= int(age_text) <= 120):
            self.app_ref.message("Inserisci un'età compresa tra 1 e 120 anni.")
            return
        sex = self.profile_sex.text
        if sex == "Sesso (facoltativo)":
            sex = ""
        self.app_ref.store.data["profile"] = {
            "name": name,
            "sex": sex,
            "age": age_text,
        }
        self.app_ref.store.save()
        self.app_ref.message("Profilo salvato.")


class GymTrackerApp(App):
    title = "InForma"

    def build(self):
        Window.clearcolor = BG
        self.store = DataStore(os.path.join(self.user_data_dir, "gym_tracker.json"))
        self.active_workout = None
        self.manager = ScreenManager()
        self.home_screen = HomeScreen(self)
        self.current_plans_screen = PlansScreen(self)
        self.analytics_screen = AnalyticsScreen(self)
        self.history_screen = HistoryScreen(self)
        self.settings_screen = SettingsScreen(self)
        self.workout_screen = WorkoutScreen(self)
        for screen in (
            self.home_screen, self.current_plans_screen,
            self.analytics_screen, self.history_screen,
            self.settings_screen, self.workout_screen,
        ):
            self.manager.add_widget(screen)
        return self.manager

    def current_plan(self):
        plans = self.store.data["plans"]
        current_id = self.store.data["current_plan_id"]
        plan = next((item for item in plans if item["id"] == current_id), None)
        if plan is None:
            if not plans:
                plan = {
                    "id": "plan-1",
                    "name": "La mia scheda",
                    "days": [
                        {"id": "day-1", "name": "Giorno 1", "exercises": []},
                        {"id": "day-2", "name": "Giorno 2", "exercises": []},
                        {"id": "day-3", "name": "Giorno 3", "exercises": []},
                    ],
                    "selected_day_id": "day-1",
                }
                plans.append(plan)
            else:
                plan = plans[0]
            self.store.data["current_plan_id"] = plan["id"]
        DataStore.normalize_plan(plan)
        return plan

    @staticmethod
    def selected_day(plan):
        DataStore.normalize_plan(plan)
        return next(day for day in plan["days"] if day["id"] == plan["selected_day_id"])

    def start_workout(self, day_id=None):
        plan = self.current_plan()
        day = next(
            (item for item in plan["days"] if item["id"] == day_id),
            self.selected_day(plan),
        )
        plan["selected_day_id"] = day["id"]
        self.active_workout = {
            "plan_id": plan["id"],
            "plan_name": plan["name"],
            "day_id": day["id"],
            "day_name": day["name"],
            "exercises": [
                {"name": exercise["name"],
                 "notes": exercise.get("notes", ""),
                 "sets": [{"reps": "", "weight": ""} for _ in range(exercise.get("sets", 3))]}
                for exercise in day["exercises"]
            ],
                "exercise_index": 0,
        }
        self.go("workout")

    def go(self, screen_name):
        self.manager.current = screen_name

    def message(self, text):
        content = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))
        content.add_widget(ui_label(text, 14, TEXT, height=dp(65)))
        popup = Popup(title="InForma", content=content, size_hint=(0.82, 0.3))
        content.add_widget(make_button("OK", lambda *_: popup.dismiss()))
        popup.open()

    def quick_stats(self):
        current_id = self.current_plan()["id"]
        reset_at = self.store.data["settings"].get("workout_counter_reset_at")
        reset_time = datetime.fromisoformat(reset_at) if reset_at else None
        sessions = []
        for session in self.store.data["sessions"]:
            if session.get("plan_id") != current_id:
                continue
            completed_at = session.get("completed_at", session["date"])
            if reset_time and datetime.fromisoformat(completed_at) <= reset_time:
                continue
            sessions.append(session)
        last = "ancora nessuno"
        if sessions:
            last_date = max(item["date"] for item in sessions)
            last = datetime.fromisoformat(last_date).strftime("%d/%m/%Y")
        return {"workouts": len(sessions), "last": last}

    def exercise_bests(self):
        bests = {}
        for session in self.store.data["sessions"]:
            if session.get("plan_id") != self.store.data["current_plan_id"]:
                continue
            for exercise in session["exercises"]:
                if exercise["sets"]:
                    best = max(item["weight"] for item in exercise["sets"])
                    bests[exercise["name"]] = max(bests.get(exercise["name"], 0), best)
        return bests

    def recent_exercise_progress(self, name):
        cutoff = date.today() - timedelta(days=60)
        per_day = {}
        for session in self.store.data["sessions"]:
            if session.get("plan_id") != self.store.data["current_plan_id"]:
                continue
            session_day = date.fromisoformat(session["date"])
            if session_day < cutoff:
                continue
            for exercise in session["exercises"]:
                if exercise["name"] == name and exercise["sets"]:
                    best = max(item["weight"] for item in exercise["sets"])
                    per_day[session["date"]] = max(per_day.get(session["date"], 0), best)
        return sorted(per_day.items())

    def recent_body_weight(self):
        cutoff = date.today() - timedelta(days=60)
        return sorted(
            (item["date"], item["weight"])
            for item in self.store.data["body_weight"]
            if date.fromisoformat(item["date"]) >= cutoff
        )


if __name__ == "__main__":
    GymTrackerApp().run()
