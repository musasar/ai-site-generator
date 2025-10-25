Here is a simple interactive JavaScript code to create a "string" website:
```html
<!-- index.html -->
<!DOCTYPE html>
<html>
<head>
  <title>String Website</title>
  <script src="index.js"></script>
</head>
<body>
  <h1 id="result">?</h1>
</body>
</html>
```

```javascript
// index.js
const resultElement = document.getElementById('result');

function loadString() {
  console.log('string loaded!');
}

window.addEventListener('load', () => {
  loadString();
});
```
Let me explain what's happening:

* We have an HTML file (`index.html`) with a simple `<h1>` element and a script tag that points to our JavaScript file (`index.js`).
* In the `index.js` file, we get a reference to the `<h1>` element using `document.getElementById('result')`.
* We define a function `loadString()` that simply logs a message to the console when called.
* We use the `window.addEventListener('load', ...)` method to attach an event listener to the `load` event of the window. This event is triggered when the page finishes loading.
* When the page loads, our `loadString()` function is called, which logs the message "string loaded!" to the console.

When you run this code and load the page in your browser, you should see the message "string loaded!" logged to the console. The `<h1>` element on the page will initially display a question mark (`?`), but you can modify the `index.js` file to update the text displayed in the `<h1>` element based on user input or other interactions.