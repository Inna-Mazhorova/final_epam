// POST method
async function postJSON(url = "", data = {}) {
  const response = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return response.json();
}

async function launch() {
  const input_code = document.getElementById("code").value;
  const input_stdin = document.getElementById("input").value;

  const jsonRequestData = {
    input_code: input_code,
    input_stdin: input_stdin,
  };
  const jsonResponseData = await postJSON("/compile", jsonRequestData);

  document.getElementById("output").innerHTML = jsonResponseData.output;
  document.getElementById("error").innerHTML = jsonResponseData.error;
}
