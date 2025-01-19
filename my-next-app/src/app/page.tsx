import "bootstrap/dist/css/bootstrap.min.css";

import { config } from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";
config.autoAddCss = false;

import "./globals.css";


import SignInPage from "./pages/SignInPage";
import OptionsPage from "./pages/OptionsPage";



export default function Home() {
  return (
    <>

        <OptionsPage/>
    </>
  );
}
