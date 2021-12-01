const styleInvalidFeedbackInput = `
    border-color: #dc3545;
    padding-right: calc(1.5em + 0.75rem);
    background-repeat: no-repeat;
    background-position: right calc(0.375em + 0.1875rem) center;
    background-size: calc(0.75em + 0.375rem) calc(0.75em + 0.375rem);
`;

const formRegister = document.querySelector(".form-register");

if ( formRegister ) {
	const btnSubmit = formRegister.querySelector(".form-register-btn");

	formRegister.addEventListener("submit", (event) => {
		const passwordInput = formRegister.querySelector(".form-register-password");
		const passwordRepeatInput = formRegister.querySelector(".form-register-repeat_password");

		const passwordValue = passwordInput.value;
		const passwordRepeatValue = passwordRepeatInput.value;

		if ( passwordValue !==  passwordRepeatValue ) {
			event.preventDefault();

			const invalidFeedback = formRegister.querySelector('.form-register-invalid-feedback');
			invalidFeedback.style.display = "block";

			passwordInput.style.cssText = styleInvalidFeedbackInput;
			passwordRepeatInput.style.cssText = styleInvalidFeedbackInput;
		}
	}, true);
}
