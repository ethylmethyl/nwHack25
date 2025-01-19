const SignUpPage = () => {
  return(
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
                            <div className="flex text-[#272424] text-[16px] font-inter font-normal pt-6">Sign In</div>
                        </div>
    
                        <h1 className="text-[#272424] text-[46px] font-inter font-bold break-words pt-3">Join Homi!</h1>
                        <h2 className="w-40 text-[#8E7979] text-[34px] font-inter font-normal break-words">Let's get you an account for the most convinient housing</h2>
    
                        <div className="flex flex-row w-40 h-16 justify-start gap-5">
                            <div className="flex w-16 h-16 bg-white shadow-lg rounded-full">
                                <img 
                                    className="flex justify-center align-middle w-14 h-14 pt-2 pl-2"
                                    src="/images/Frame.svg" 
                                    alt="pfp"
                                />
                            </div>
                            <div className="flex-col justify-start align-middle gap-1">
                                <p className="text-[#8E7979] text-[20px] font-inter font-normal">Add a Profile Picture</p>
                                <div className=""></div>
                            </div>
                        </div>

                        {/* <SignInForm /> */}
    

                        <div className=" text-[#8E7979] text-[12px] font-inter font-normal break-words">By continuing, you agree to our Terms of Service and Privacy Policy.</div>
                    </div>
    
                    <img 
                    className="flex justify-center align-middle w-96 h-96 " 
                    src="/images/house logo.png" 
                    alt="House Logo"
                    />
                
                </div>
            </div>
  );
};
