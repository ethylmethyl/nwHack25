import "bootstrap/dist/css/bootstrap.min.css";

import { config } from "@fortawesome/fontawesome-svg-core";
import "@fortawesome/fontawesome-svg-core/styles.css";
config.autoAddCss = false;

import "./globals.css";

// import NoSsr from "./components/next/NoSSR";
// import { ConnectToX } from "./components/SignInComponents/ConnectToX";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faGoogle } from "@fortawesome/free-brands-svg-icons";
import SignInPage from "./pages/SignInPage";

export default function Home() {
  return (
    <>
     {/*<NoSsr>
       <SignInForm />
     </NoSsr>/*}
      {/* <ConnectToX logo={faGoogle} label={"Connect to Google"} /> */}
        <SignInPage/>
    </>
  );
}
