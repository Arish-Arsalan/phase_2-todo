import express from "express";
import cors from "cors";
import router from "./routes/todos.js";

const app = express();
app.use(cors());
app.use(express.json());
app.use("/todos", router);

const PORT = 3000;

const server = app
  .listen(PORT)
  .on("listening", () => {
    console.log(`Server running on port ${PORT}`);
    console.log(`Running on port: ${server.address().port}`);
  })
  .on("error", (err) => {
    if (err.code === "EADDRINUSE") {
      console.log(`Port ${PORT} is in use. Trying another port...`);

      // Start on a random free port
      const fallback = app.listen(0).on("listening", () => {
        console.log(`Server started on free port: ${fallback.address().port}`);
      });
    } else {
      throw err;
    }
  });
