const { app, BrowserWindow } = require("electron");

function createWindow() {
  // Arquivo inicial de Start Windows Aplication
  let win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: true,
    },
  });

  // Carrega o arquivo index.html da aplicação.
  win.loadURL("http://localhost:3000");
}

app.whenReady().then(createWindow);
