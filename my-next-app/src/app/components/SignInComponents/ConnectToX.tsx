import Button from 'react-bootstrap/Button';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';


export const ConnectToX = ({logo, label}) => {
    return (
        <div className="w-full h-12 ">
            <Button variant="light" className='py-2 flex flex-row w-[80%] justify-items-center bg-white'>
                <FontAwesomeIcon icon={logo} className='mr-6'/> {label}
            </Button>

{/*             
            <div className="flex flex-row justify-items-center">
                <div className=" border-flex justify-start w- h- text-[#272424] text-[16px] font-inter font-normal break-words">Continue with Google</div>
            </div> */}
        </div> 
    )
}