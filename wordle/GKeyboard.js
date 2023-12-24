/**
 * GKeyboard.js
 * =============
 * (For students working on assignment 3, Wordle: Feel free to study this code,
 *  but you can get everything you need from the comments below.)
 *
 * (For students working on assignment 4, Enigma: Feel free to study this code,
 *  but don't copy it; I *promise* it is easier to implement the keyboard
 *  yourself from scratch as the handout suggests than it is to repurpose this.)
 */

const KEYBOARD_MARGIN = 4;
const KEYBOARD = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"];
const KEYBOARD_FONT = "400 24px HelveticaNeue";

/**
 * GKeyboard
 * Usage: let keyboard = GKeyboard(x, y, width, textColor, defaultColor);
 * =======================================================================
 * Creates a clickable keyboard of the given width. It exposes some events you
 * can use to respond to user interaction. See method definitions below.
 */
function GKeyboard(x, y, width, textColor, defaultColor) {
  /**
   * keyboard.addEventListener(event, callback);
   * --------------------------------------------
   * Calls the function `callback` when the specified event happens.
   * -> Event "keyclick"
   *     -  Happens whenever the user clicks on a lettered keyboard key.
   *       Passes the key clicked (lowercase single character) as the
   *       first argument to the callback function.
   * -> Event "enter"
   *     -  Happens whenever the user clicks on the enter/return button.
   * -> Event "backspace"
   *     - Happens whenever the user clicks on the backspace button.
   */
  function addEventListener(type, cb) {
    if (type === "keyclick") {
      keyClickListeners.push(cb);
    } else if (type === "enter") {
      enterListeners.push(cb);
    } else if (type === "backspace") {
      backspaceListeners.push(cb);
    }
  }

  /**
   * keyboard.setKeyColor(letter, color);
   * -------------------------------------
   * Sets the key of the given letter to the specified color.
   * Throws an error if the given letter is invalid.
   */
  function setKeyColor(key, color) {
    key = key.toLowerCase();
    if (!Object.keys(keys).includes(key)) {
      throw new Error(`Key ${key} is not a valid keyboard key`);
    }

    keys[key].rect.setColor(color);
  }

  /**
   * keyboard.getKeyColor(letter);
   * ------------------------------
   * Retrieves the color of the key with the given letter.
   */
  function getKeyColor(key) {
    key = key.toLowerCase();
    if (!Object.keys(keys).includes(key)) {
      throw new Error(`Key ${key} is not a valid keyboard key`);
    }

    return keys[key].rect.getColor();
  }

  // IMPLEMENTATION FOLLOWS
  // Students: feel free to study this, but also keep in mind that this is
  //           fairly janky (since I'm sort of forcing my way hooking into
  //           the graphics library). You won't have to do anything like this
  //           in CS106AX.

  // Setup variables
  const compound = GCompound(x, y);
  const squareSize = GKeyboard.getSquareSize(width);
  const origSetParent = compound._setParent.bind(compound);

  // Keyboard state
  const keys = {};
  const keyClickListeners = [];
  const enterListeners = [];
  const backspaceListeners = [];
  let parent = null;

  function createKeyboardKey(key, x, y, width) {
    if (width === undefined) width = squareSize;

    const compound = GCompound(x, y);
    const rect = GRect(width, squareSize);
    rect.setFilled(true);
    rect.setColor(defaultColor);
    const label = GLabel(key, width / 2, squareSize / 2);
    label.setFont(KEYBOARD_FONT);
    label.setColor(textColor);
    label.setBaseline("middle");
    label.setTextAlign("center");

    compound.add(rect);
    compound.add(label);

    return { rect, label, compound };
  }

  for (let row = 0; row < KEYBOARD.length; row++) {
    const y = 0 + KEYBOARD_MARGIN * (2 * row + 1) + squareSize * row;
    const rowKeys = KEYBOARD[row];
    const rowWidth =
      KEYBOARD_MARGIN * 2 * rowKeys.length + squareSize * rowKeys.length;

    const startX = (width - rowWidth) / 2;

    for (let col = 0; col < rowKeys.length; col++) {
      const x = startX + KEYBOARD_MARGIN * (2 * col + 1) + squareSize * col;

      const keyInfo = createKeyboardKey(rowKeys[col], x, y);
      keys[rowKeys[col].toLowerCase()] = keyInfo;
      compound.add(keyInfo.compound);
    }
  }

  const enter = createKeyboardKey(
    "⏎",
    0,
    KEYBOARD_MARGIN * 5 + squareSize * 2,
    squareSize * 1.5
  );
  compound.add(enter.compound);

  const backspace = createKeyboardKey(
    "←",
    width - squareSize * 1.5,
    KEYBOARD_MARGIN * 5 + squareSize * 2,
    squareSize * 1.5
  );
  compound.add(backspace.compound);

  function onClick(e) {
    for (const key of Object.keys(keys)) {
      const { compound } = keys[key];
      if (compound.contains(e.getX() - x, e.getY() - y)) {
        keyClickListeners.forEach((cb) => cb(key));
      }
    }
    if (enter.compound.contains(e.getX() - x, e.getY() - y)) {
      enterListeners.forEach((cb) => cb());
    }
    if (backspace.compound.contains(e.getX() - x, e.getY() - y)) {
      backspaceListeners.forEach((cb) => cb());
    }
  }

  // Overwrite protected function to get the GWindow so we can add an event
  //  listener to it.
  compound._setParent = function (newParent) {
    parent = newParent;
    while (parent._getParent && parent._getParent()) {
      parent = parent._getParent();
    }
    parent.addEventListener("click", onClick);
    origSetParent(newParent);
  };

  compound.addEventListener = addEventListener;
  compound.setKeyColor = setKeyColor;
  compound.getKeyColor = getKeyColor;

  return compound;
}
/**
 * GKeyboard.getSquareSize(width);
 * --------------------------------
 * Retrieves the number of pixels wide each keyboard key will be.
 * (students: you probably won't need to use this.)
 */
GKeyboard.getSquareSize = function (width) {
  return (width - KEYBOARD_MARGIN * 2 * 10) / 10;
};

/**
 * GKeyboard.getHeight(width);
 * ----------------------------
 * Retrieves the height of the keyboard given its width.
 * (students: you probably won't need to use this.)
 */
GKeyboard.getHeight = function (width) {
  return 3 * GKeyboard.getSquareSize(width) + 6 * KEYBOARD_MARGIN;
};
