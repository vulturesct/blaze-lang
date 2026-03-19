# 🔥 Blaze Programming Language

> ⚠️ **Early Development** — Blaze is currently in early development. Expect bugs, missing features, and big updates coming soon!

A fast, powerful, and easy to learn programming language built for games, apps, and software.

> Made by [vulturesct](https://github.com/vulturesct)

---

## What is Blaze?

Blaze is a programming language designed to be **powerful yet simple**. Whether you want to make a game, build an app, or write scripts — Blaze has you covered.

```
-- Hello World in Blaze
let name = "World"
print("Hello " + name)
```

---

## Features

- 🔥 Simple, clean syntax — easy to learn
- 🎮 Built-in game engine — draw shapes, handle keyboard input
- 📋 Lists, math, and string functions built in
- 🔁 Loops, functions, if/else
- 💬 User input
- ⚡ Fast to write, fast to run

---

## Requirements

- Python 3.10 or higher
- No extra installs needed

---

## Installation

1. Download or clone this repo:
```
git clone https://github.com/vulturesct/blaze-lang
```

2. Make sure Python is installed:
```
python --version
```

3. Run a Blaze file:
```
py blaze.py yourfile.blz
```

Or just **double click or if its not working run as administrator `run.bat`** and pick your `.blz` file!

---

## Writing Blaze Code

Blaze files end in `.blz`. You can write them in any text editor:

- **Notepad** — already on your PC, just save as `.blz`
- **Notepad++** — free download, better than Notepad, recommended for beginners
- **VS Code** — free, best option for more advanced users

> 💡 A dedicated Blaze editor (Ember) is coming in a future update!

---

## Syntax Guide

### Variables
```
let name = "Blaze"
let age = 17
let pi = 3.14
```

### Print
```
print("Hello!")
print("Name: " + name)
```

### If / Else
```
if age > 10 {
    print("old enough")
} else {
    print("too young")
}
```

### Loops
```
-- Loop a number of times
loop 5 times {
    print("repeating!")
}

-- Loop while condition is true
loop while age < 18 {
    set age = age + 1
}

-- Loop through a list
let items = ["sword", "shield", "potion"]
loop each item in items {
    print(item)
}
```

### Functions
```
func greet(name) {
    print("Hello " + name)
}

greet("World")
```

### Lists
```
let nums = [1, 2, 3]
add(nums, 4)
remove(nums, 0)
let first = get(nums, 0)
let count = size(nums)
```

### Math
```
let x = sqrt(16)
let y = pow(2, 8)
let z = abs(-5)
let r = round(3.7)
let n = random(1, 100)
```

### Strings
```
let up = upper("hello")
let lo = lower("HELLO")
let n  = length("blaze")
```

### User Input
```
include input

let name = input("What is your name?")
print("Hello " + name)
```

---

## Game Development

Blaze has a built-in game engine!

```
include draw

let px = 380
let py = 280

game.loop {
    draw.clear()
    if key("left") {
        set px = px - 5
    }
    if key("right") {
        set px = px + 5
    }
    if key("up") {
        set py = py - 5
    }
    if key("down") {
        set py = py + 5
    }
    draw.rect(px, py, 40, 40, "white")
}
```

### Draw Commands
| Command | Description |
|---|---|
| `draw.rect(x, y, w, h, color)` | Draw a rectangle |
| `draw.circle(x, y, radius, color)` | Draw a circle |
| `draw.text(x, y, text, color)` | Draw text |
| `draw.clear()` | Clear the screen |
| `draw.bgcolor(color)` | Set background color |

### Key Names
`left` `right` `up` `down` `space` `return` `a`-`z` `0`-`9`

---

## Example Programs

### Guessing Game
```
include input

let secret = random(1, 10)
let guess = 0

loop while guess != secret {
    let guess = num(input("Guess a number 1-10:"))
    if guess < secret {
        print("Too low!")
    }
    if guess > secret {
        print("Too high!")
    }
}

print("You got it!")
```

### Dot Collector Game
```
include draw

let px = 380
let py = 280
let ex = 100
let ey = 100
let score = 0

game.loop {
    draw.clear()
    if key("left") { set px = px - 5 }
    if key("right") { set px = px + 5 }
    if key("up") { set py = py - 5 }
    if key("down") { set py = py + 5 }
    if near(px, py, ex, ey, 40) {
        set score = score + 1
        set ex = random(50, 750)
        set ey = random(50, 550)
    }
    draw.rect(px, py, 40, 40, "white")
    draw.circle(ex, ey, 15, "yellow")
    draw.text(100, 20, "Score: " + score, "white")
}
```

---

## Roadmap

- [ ] Ember IDE — a modern code editor built for Blaze
- [ ] Better error messages
- [ ] More math and string functions
- [ ] Sound module
- [ ] Web module
- [ ] Package to .exe

---

## Copyright

Please dont download it and duplicate it edit it and finish yourself, this is my own project. If you would like to collaborate atleast message me on discord user: vulturewashere.

--

## License

MIT License — free to use, modify, and share.

---

## Contributing

Pull requests are welcome! If you want to add features, fix bugs, or improve docs — go for it.

---

*Blaze — set your code on fire* 🔥
