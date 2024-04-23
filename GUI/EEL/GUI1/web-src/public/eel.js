class Eel {
  /* 
  This  is for testing online.
  Here are placeholders of the eel functions
  so that the front-end can be tested with 'yarn dev'
  */

  close_python = () => {
    console.log("closing python");
  };

  create_5_jokes = (topic) => (func) => {
    const output = [
      {
        setup: topic + " 1",
        punchline: "punchline 1",
      },
      {
        setup: topic + " 2",
        punchline: "punchline 2",
      },
      {
        setup: topic + " 3",
        punchline: "punchline 3",
      },
      {
        setup: topic + " 4",
        punchline: "punchline 4",
      },
      {
        setup: topic + " 5",
        punchline: "punchline 6",
      },
    ];
    return func(output);
  };

  generate_voice = (jokes, filename, type) => (func) => {
    console.log(jokes);
    console.log(filename);
    console.log(type);
    const output = `./output/${filename}.mp3`;
    return func(output);
  };

  play_voice = (filename) => {
    console.log("play sound: " + filename);
  };

  open_folder = () => {
    console.log("open folder");
  };
}

const eel = new Eel();
