import time
from typing import Tuple, Callable, Optional
from dataclasses import dataclass
from pynput import mouse, keyboard

@dataclass
class GuiData:
    """State class for obtained data from user about gui chat"""
    chat_name: Optional[str]

class Gui:
    """Namespace for gui methods"""
    @staticmethod
    def block_for_mouse_down() -> Tuple[int, int]:
        def handler(x: int, y: int, button: mouse.Button, pressed: bool) -> bool:
            if button == mouse.Button.left or button == mouse.Button.right:
                return False
            else:
                return True
        
        listener = mouse.Listener(on_click=handler)
        listener.start()
        listener.join()
        controller = mouse.Controller()
        print(controller.position)
        return controller.position
    
    @staticmethod
    def click_at_position(position: Tuple[int, int], delay: float=0.1):
        controller = mouse.Controller()
        controller.position = position
        time.sleep(delay)
        controller.click(mouse.Button.left)
    
    @staticmethod
    def type_characters(chars: str, delay_fn: Callable[[], float]=lambda: 0):
        time.sleep(delay_fn())
        controller = keyboard.Controller()
        for letter in chars:
            controller.press(letter)
            controller.release(letter)
            time.sleep(delay_fn())

    @staticmethod
    def find_coordinates_of_text_on_screen(search_string: str) -> Tuple[int, int]:
        return (0, 0)