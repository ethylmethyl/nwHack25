
import { faFacebook, faGoogle, faMicrosoft, faXTwitter } from "@fortawesome/free-brands-svg-icons";
import { ConnectToX } from "../components/SignInComponents/ConnectToX";
import { FieldForm } from "../components/SignInComponents/FieldForm";



const SignInPage = () => {

    return (  
        // top row: logo + signup button
        <div className="w-full h-full relative bg-[#FCFCFC]">
            <div className="flex flex-row justify-center pt-16">
                <div className="w-[45vw] flex flex-col justify-center gap-1">
                    <div className="flex flex-row w-full h-16 justify-start gap-[25vw]">
                        <div className="flex w-16 h-16 bg-white shadow-lg rounded-full">
                            <img 
                                className="flex justify-center align-middle w-14 h-14 pt-2 pl-2"
                                src="/images/house logo.png" 
                                alt="House Logo"
                            />
                        </div>
                        <div className="flex text-[#272424] text-[16px] font-inter font-normal pt-6">Sign up</div>
                    </div>

                    <h1 className="text-[#272424] text-[46px] font-inter font-bold break-words pt-3">Hello Again!</h1>
                    <h2 className="text-[#272424] text-[28px] font-inter font-normal break-words">Sign in to Homi</h2>

                    <FieldForm label={"Email"} placeholder={"Type your email here"}/>
                    <FieldForm label={"Password"} placeholder={"Type your password here"}/>

                    <button className="w-[80%] h-10 rounded-md mt-2 bg-black text-white text-[14px]">Sign In</button>

                    <div className="mt-4">
                        <ConnectToX logo={faGoogle} label={"Connect to Google"}/>
                        <ConnectToX logo={faMicrosoft} label={"Connect to Microsoft"}/>
                        <ConnectToX logo={faFacebook} label={"Connect to Facebook"}/>
                        <ConnectToX logo={faXTwitter} label={"Connect to Twitter"}/>
                    </div>

                    <div className=" text-[#8E7979] text-[12px] font-inter font-normal break-words">By continuing, you agree to our Terms of Service and Privacy Policy.</div>
                    <div className=" text-[#8E7979] text-[16px] font-inter font-normal break-words">Forgot password?</div>
                </div>


                <img 
                className="flex justify-center align-middle w-96 h-96 " 
                src="/images/house logo.png" 
                alt="House Logo"
                />

            
            </div>
        </div>
    )
} 

export default SignInPage;                      