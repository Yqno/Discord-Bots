const Discord = require('discord.js');
const client = new Discord.Client();

// Ein Objekt, um die Kontostände der Nutzer zu speichern
const userAccounts = {};

client.on('ready', () => {
  console.log(`Eingeloggt als ${client.user.tag}`);
});

client.on('message', message => {
  // Überprüfe, ob der Befehl "!roulette" aufgerufen wurde
  if (message.content.startsWith('!roulette')) {
    // Extrahiere den Einsatz aus der Nachricht
    const args = message.content.split(' ');
    const betAmount = parseInt(args[1]);

    // Überprüfe, ob ein gültiger Einsatzbetrag angegeben wurde
    if (!betAmount || betAmount <= 0) {
      message.reply('Bitte gib einen gültigen Einsatzbetrag an!');
      return;
    }

    // Überprüfe, ob der Nutzer genug Geld hat, um zu wetten
    const userID = message.author.id;
    if (!userAccounts[userID] || userAccounts[userID] < betAmount) {
      message.reply('Du hast nicht genug Geld, um diese Wette zu platzieren!');
      return;
    }

    // Simuliere das Drehen des Rouletterads
    const number = Math.floor(Math.random() * 37);

    // Berechne den Gewinn des Nutzers
    let winnings = 0;
    if (number === 0) {
      // Wenn die Nummer 0 ist, gewinnt der Nutzer nichts
      winnings = 0;
    } else {
      // Wenn die Nummer ungleich 0 ist, gibt es einen Gewinner
      winnings = betAmount * 36;
    }

    // Ziehe den Einsatzbetrag vom Kontostand des Nutzers ab
    userAccounts[userID] -= betAmount;

    // Füge den Gewinn dem Kontostand des Nutzers hinzu
    userAccounts[userID] += winnings;

    // Antworte dem Nutzer mit dem Ergebnis
    if (winnings === 0) {
      message.reply(`Die Nummer ist ${number}. Du hast nichts gewonnen!`);
    } else {
      message.reply(`Die Nummer ist ${number}. Herzlichen Glückwunsch, du hast ${winnings} gewonnen!`);
    }
  }

  // Überprüfe, ob der Befehl "!balance" aufgerufen wurde
  if (message.content.startsWith('!balance')) {
    const userID = message.author.id;

    // Überprüfe, ob der Nutzer ein Konto hat
    if (!userAccounts[userID]) {
      message.reply('Du hast noch kein Konto. Bitte spiele Roulette, um ein Konto zu erstellen.');
      return;
    }

    // Gib den aktuellen Kontostand des Nutzers aus
    message.reply(`Du hast ${userAccounts[userID]} Coins auf deinem Konto.`);
  }
});

client.login('DEIN_DISCORD_BOT_TOKEN');
