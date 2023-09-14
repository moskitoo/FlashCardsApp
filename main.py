from typing import Callable, Tuple, List, Dict, Hashable, Any
from random import choice
from tkinter import Tk, PhotoImage, Canvas, Button
import pandas




class WindowConfiguration:
    BACKGROUND_COLOR = "#B1DDC6"

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Flashy")
        self.window.config(padx=50, pady=50, bg=self.BACKGROUND_COLOR)
        self.reset_timer()

    def reset_timer(self, callback: Callable[[], None] = lambda: ...) -> None:
        self.timer = self.window.after(3000, callback)

    def back_to_previous_state(self) -> None:
        self.window.after_cancel(self.timer)

    def run(self) -> None:
        self.window.mainloop()


class CanvasConfiguration:
    def __init__(self, card_front_name: PhotoImage) -> None:
        self.canvas = Canvas(width=800,
                             height=536,
                             bg=WindowConfiguration.BACKGROUND_COLOR,
                             highlightthickness=0)
        self.canvas.grid(column=0, row=0, columnspan=2)
        self.canvas_image = self.canvas.create_image(
            400, 
            536 / 2, 
            image=card_front_name)
        self.title_text = None
        self.word_text = None

    def configure(self) -> None:
        self.title_text = self.canvas.create_text(
            400, 150, text="", font=("Ariel", 40, "italic"))
        self.word_text = self.canvas.create_text(
            400, 236, text="", font=("Ariel", 60, "bold"))

    def configure_item(self, tagOrId: str, **kwargs) -> None:
        self.canvas.itemconfig(tagOrId, **kwargs)


class LanguageCanvas:
    def __init__(self,
                 language: str,
                 fill: str,
                 card_name: PhotoImage,
                 canvas_config: CanvasConfiguration) -> None:
        self.language = language
        self.fill = fill
        self.card_name = card_name
        self.canvas_config = canvas_config

    def set_canvas(self, word):
        self.canvas_config.configure_item(
            self.canvas_config.word_text, text=word[self.language], fill=self.fill)
        self.canvas_config.configure_item(
            self.canvas_config.title_text,
            text=self.language,
            fill=self.fill)
        self.canvas_config.configure_item(
            self.canvas_config.canvas_image,
            image=self.card_name)


class WordManager:

    def __init__(self, new_word_language_canvas: LanguageCanvas,
                 flip_card_language_canvas: LanguageCanvas,
                 words: List[Dict[Hashable, Any]],
                 window_config: WindowConfiguration) -> None:
        self.new_word_language_canvas = new_word_language_canvas
        self.flip_card_language_canvas = flip_card_language_canvas
        self.words = words
        self.current_word = ''
        self.window_config = window_config
        self.window_config.reset_timer(self.flip_card)

    def choice_word(self):
        self.current_word = choice(self.words)

    def new_word(self) -> None:
        self.reset_word_timer()
        self.choice_word()
        self.set_current_word_on_canvas()

    def set_current_word_on_canvas(self):
        self.new_word_language_canvas.set_canvas(self.current_word)
        self.window_config.reset_timer(self.flip_card)

    def reset_word_timer(self):
        self.window_config.back_to_previous_state()

    def flip_card(self) -> None:
        self.flip_card_language_canvas.set_canvas(self.current_word)

    def is_known(self) -> None:
        self.remove_known_word()
        self.create_csv()
        self.new_word()

    def create_csv(self):
        data = pandas.DataFrame(self.words)
        data.to_csv("data/words_to_learn_french.csv", index=False)

    def remove_known_word(self):
        self.words.remove(self.current_word)


class WordProvider:

    @staticmethod
    def get_words(path: str, 
                  default_path='data/french_words.csv') -> Tuple[pandas.DataFrame, 
                                                                 List[Dict[Hashable, Any]]]:
        try:
            words_df = pandas.read_csv(path)
        except FileNotFoundError:
            words_df = pandas.read_csv(default_path)
        finally:
            words = words_df.to_dict(orient="records")
        return words_df, words


class GridConfiguration:
    def __init__(self, row: int, column: int) -> None:
        self.row = row
        self.column = column


class ImagedButton:
    def __init__(self, img_path: str, cmd: Callable[[
    ], None], grid_config: GridConfiguration) -> None:
        self.image = PhotoImage(file=img_path)
        self.button = Button(
            image=self.image,
            highlightthickness=0,
            command=cmd)
        self.button.grid(column=grid_config.column, row=grid_config.row)


class FlashyApplication:
    def __init__(self) -> None:
        self.words_df, self.words = WordProvider.get_words(
            "data/words_to_learn_french.csv")
        self.languages = list(self.words_df.columns.values)

        self.window_config = WindowConfiguration()
        self.card_front_name = PhotoImage(file="images\\card_front.png")
        self.canvas_config = CanvasConfiguration(self.card_front_name)

        self.new_word_language_canvas = LanguageCanvas(language=self.languages[0],
                                                       fill='black',
                                                       card_name=self.card_front_name,
                                                       canvas_config=self.canvas_config)
        self.filp_car_language_canvas = LanguageCanvas(language=self.languages[1],
                                                       fill='white',
                                                       card_name=PhotoImage(
                                                           file="images/card_back.png"),
                                                       canvas_config=self.canvas_config)

        self.word_mngr = WordManager(self.new_word_language_canvas,
                                     self.filp_car_language_canvas,
                                     words=self.words,
                                     window_config=self.window_config)

        self.right_imaged_btn = ImagedButton(img_path="images/right.png",
                                             cmd=self.word_mngr.is_known, 
                                             grid_config=GridConfiguration(row=1, column=1))
        self.wrong_imaged_btn = ImagedButton(img_path="images/wrong.png",
                                             cmd=self.word_mngr.new_word,
                                             grid_config=GridConfiguration(row=1, column=0))

        self.canvas_config.configure()

    def run(self):
        self.word_mngr.new_word()
        self.window_config.run()


if __name__ == '__main__':
    app = FlashyApplication()
    app.run()
