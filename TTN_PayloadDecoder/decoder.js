function Decoder(bytes, port) {

    // Get the string "111 014" out of the bytes 3131312030313400
    var text = String.fromCharCode.apply(null, bytes);

    // Split into an array of 2 strings, on the space character
    var values = text.split(" ");

    // Return as true numbers
    return {
      Floor_No: (values[0]),
      Status: (values[1])
    }
}