require("dotenv").config();
const express = require("express");
const app = express();
const session = require("express-session");
const path = require("path");
const passport = require("passport");
require("./config/passport.js");
//Router imports
const authRouter = require("./routes/auth.routes.js");
const acpRouter = require("./routes/acp.routes.js");

app.use(express.json());//for reading json requests
app.use(express.urlencoded({extended: true}));//to parse HTML Forms data
app.use(express.static(path.join(__dirname,"../../frontend")));//static files (frontend css and js files) are made available publically

//Express Session
const sessionOptions = {
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: true,
    cookie: {
        expires: Date.now() + 24*60*60*1000,
        maxAge: 24*60*60*1000,
        httpOnly: true
    }
};
app.use(session(sessionOptions));

//Passport initialization and session enabling
app.use(passport.initialize());
app.use(passport.session());

//Server listening for requests
app.listen(process.env.PORT,()=>{
    console.log("server listening");
});

//Login Routes
app.use('/auth', authRouter);
//ACP Routes
app.use('/', acpRouter);