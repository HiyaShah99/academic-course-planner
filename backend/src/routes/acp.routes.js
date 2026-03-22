const express = require("express");
const router = express.Router();
const { isLoggedIn } = require("../middleware");
const path = require("path");

//authentication before allowing access to the main page
router.use(isLoggedIn);

//Index route: access the main page
router.get('/', (req,res)=>{
    res.sendFile(path.join(__dirname,"../../../frontend/main/index.html"));
});

module.exports = router;