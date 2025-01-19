import NavBarComp from "../components/NavBarComp";
import Button from 'react-bootstrap/Button';


const OptionsPage = () => {
    return (
        <div className="relative">
           
           <NavBarComp/>

            <div className="flex flex-row gap-16 justify-center align-middle">
                <div className="flex max-h-full w-[30vw] border rounded-md shadow-md bg-white py-5 my-5">
                    <div className="flex flex-col w-full content-center">
                        <div className="w-full justify-items-center"><img 
                            className= "flex w-52 h-52"
                            src="/images/house1.png" 
                            alt="House"
                        /> </div>
                        <p className="text-[#272424] text-[28px] font-inter font-bold break-words text-center w-full">Find a Place</p>
                        <p className="text-[#272424] text-[18px] font-inter font-normal break-words text-center px-5">
                            Find your house with an immersive photo experience and the most listings for student housing options.
                        </p>
                        <div className="w-full justify-items-center mb-3"><div className="bg-white w-[40%] hover:bg-[#d9d9d9] text-center text-[#2953a7] border-2 border-[#2953a7] text-[18px] font-bold font-inter py-2 mt-1 rounded-lg ">Browse Homes</div></div>
                    </div>
                </div>
                <div className="flex max-h-full w-[30vw] border rounded-md shadow-md bg-white py-5 my-5">
                    <div className="flex flex-col w-full content-center">
                        <div className="w-full justify-items-center"><img 
                            className= "flex w-52 h-52"
                            src="/images/sign.png" 
                            alt="sign"
                        /> </div>
                        <p className="text-[#272424] text-[28px] font-inter font-bold break-words text-center w-full">Sell Your Place</p>
                        <p className="text-[#272424] text-[18px] font-inter font-normal break-words text-center px-8">
                            A seamless online experience to help you effortlessly sublet or sell your home.                        
                        </p>
                        <div className="w-full justify-items-center mb-3"><div className="bg-white w-[40%] hover:bg-[#d9d9d9] text-center text-[#2953a7] border-2 border-[#2953a7] text-[18px] font-bold font-inter py-2 mt-1 rounded-lg ">Browse Homes</div></div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default OptionsPage;