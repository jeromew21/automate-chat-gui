The two backends, FF and Chrome,
have pros and cons.

Firefox:
Pros: 
    -Easy to run in headless mode (`export MOZ_HEADLESS=1`)
    -Undected by Twitter in headless
    -Generally easier to grok, follows Selenium API better
Cons:
    -Slower ish maybe
    -Can't autofocus window

Chrome:
Pros:
    -Twitter optimized
    -Can autofocus window
Cons:
    -Headless detected by Twitter

Will run benchmarks when I get stable internet.

