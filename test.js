const axios = require("axios");

// A weboldal URL-je
const url = "https://kgyte.eu";

axios
  .get(url)
  .then((response) => {
    if (response.status === 200) {
      console.log(`${url} elérhető.`);
    } else {
      console.log(`${url} nem elérhető. Állapotkód: ${response.status}`);
    }
  })
  .catch((error) => {
    console.log(`${url} nem elérhető. Hiba: ${error.message}`);
  });
