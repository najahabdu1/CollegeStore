const signUpButton = document.getElementById('signInM');
const signInButton = document.getElementById('signInA');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});

//Footer
document.getElementById('year').appendChild(document.createTextNode(new Date().getFullYear()));