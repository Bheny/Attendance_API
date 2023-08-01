from deepface import DeepFace
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, generics, ModelViewSet
from rest_framework import viewsets
from .models import Student_Register
from Authentication.models import VoterOTP
from Authentication.serializers import VoterOTPSerializer
from .serializers import VerifyVoterSerializer, StudentRegisterSerializer
from Authentication.services import generateOTP
from Authentication.models import VoterOTP
from rest_framework.decorators import action
import openpyxl 


'''
    fetch all votes that voter has casted
    let ballots = get the length of all  ballots in the election being voted on
    check if the total number of votes of the voter equals the number of ballots.
    if it equals then return true  for the has_voted.

    two .. return all voted balloted by the voter as voted_ballots
'''
class StudentRegisterUpload(viewsets.ModelViewSet):
    queryset = Student_Register.objects.all()
    serializer_class = StudentRegisterSerializer

    @action(detail=True, methods=['post']) 
    def upload_list(self, request, pk=None):
        quiz = self.get_object()
        print("im in")
        # Check if a file was uploaded
        file = request.FILES.get('file')
        if not file:
            return Response({'error': 'Please provide a file to upload.'}, status=status.HTTP_400_BAD_REQUEST)

        # Load the Excel file
        try:
            workbook = openpyxl.load_workbook(file)
            worksheet = workbook.active
        except Exception as e:
            return Response({'error': f'Failed to load the file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        # Parse the questions and answers from the Excel file
        voters = []
        for row in worksheet.iter_rows(min_row=2):
            row_data = row[0].value
            # name = row_data[0]
            details = []
            for cell in row:
                if cell.value:
                    details.append(cell.value)
                else:
                    details.append("N/A")
            voters.append(details)
            print(details)

            for voter in details:
                if details[2]:
                    voter, created = Student_Register.objects.get_or_create(voter_id=details[1],first_name=details[0],phone=details[2])
                    print(voter, created)
                    print(details)
        # Create the questions and answers
        # for question_data in questions:
        #     question = Question.objects.create(text=question_data['text'], quiz=quiz)
        #     for answer_text in question_data['answers']:
        #         is_correct = answer_text.startswith('*')
        #         answer_text = answer_text.lstrip('*')
        #         Option.objects.create(text=answer_text, is_correct=is_correct, question=question)

        return Response({'success': f'Successfully uploaded {len(voters)} students to the quiz.'})
    
    # @action(detail=True, methods=['post'])
    # def upload_answers(self, request, pk):
    #     # Get the quiz object with the given ID
    #     voter = get_object_or_404(VotersRegister, id=pk)
        
    #     # Parse the user's answers from the request body
    #     submitted_list = request.data['list']
        
    #     # Validate the user's answers
    #     if not submitted_list:
    #         return Response({'error': 'No list submitted'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     # Save the user's answers to the database
    #     for voter in submitted_list:
    #         voter_id = voter['voter_id']
    #         fn = voter['first_name']
    #         ln = voter['last_name']
    #         phone = voter['phone']
            
    #         VotersRegister.objects.create(first_name=fn, last_name=ln, phone=phone)
        
    #     # Return a success message
    #     return Response({'message': 'list submitted successfully'}, status=status.HTTP_201_CREATED)

class VotersRegisterView(generics.ListAPIView, generics.CreateAPIView , GenericViewSet):
    queryset = Student_Register.objects.all()
    serializer_class = StudentRegisterSerializer

    

class ValidateVoterId(GenericAPIView):
    queryset = Student_Register.objects.all()
    serializer_class = StudentRegisterSerializer
    
    def post(self, request):
        student_id = request.data['student_id']
        print(student_id)
        # fetch voters details
        student = self.get_serializer(get_object_or_404(Student_Register, student_id=student_id))
        # generate otp for voter
        
        # get the phone number of the voter 

        #send the otp to the phone number

        return Response(student.data)

class VerifyVoterIdentity(GenericAPIView):
    queryset = Student_Register.objects.all()
    serializer_class = VerifyVoterSerializer
    
    def post(self, request):
        """Verify Voter ID and Face

        Args:
            request (HTTP Request): receives user input

        Returns:
            Response: JSON response of voter details and OTP
        """
        serializer = VerifyVoterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        student = get_object_or_404(Student_Register, student_id=request.data["student_id"])
        student_data= StudentRegisterSerializer(student).data

        return student_data 
    
# class VerifyVoterIdentity(GenericAPIView):
    """
        Voter Identity verification
    """
    queryset = Student_Register.objects.all()
    serializer_class = VerifyVoterSerializer
    
    metrics = ["cosine", "euclidean", "euclidean_l2"]
    models = [
        "VGG-Face", 
        "Facenet", 
        "Facenet512", 
        "SFace",
        "OpenFace", 
        "DeepFace", 
        "DeepID", 
        "ArcFace", 
        "Dlib", 
    ]
    
    def post(self, request):
        """Verify Voter ID and Face

        Args:
            request (HTTP Request): receives user input

        Returns:
            Response: JSON response of voter details and OTP
        """
        serializer = VerifyVoterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        student = get_object_or_404(Student_Register, student_id=request.data["student_id"])
        student_data= StudentRegisterSerializer().data
        student_image = student_data['photo']
        image_file = request.data["photo"]
        
        df = {"verified": False}
        
        try:
            df = self.verifyVoter(image_file=image_file, student_image=student_image)
            if(df["verified"]):
                # generate otp
                # generated_otp = generateOTP()
                # voter_otp, _ = VoterOTP.objects.update_or_create(voter=voter, defaults={'otp':generated_otp})
                # send otp as part of the respo
                return Response({"student": student_data, "verified": True},
                            status=status.HTTP_202_ACCEPTED)
            return Response({"student": None, "verified": False},
                        status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("ERROR:", e)
            return Response({"student": None, "verified": False},
                        status=status.HTTP_200_OK)
        
        
    def verifyVoter(self, image_file, voter_image):
        """" 
        Verify similarity between two images
        """
        data = DeepFace.verify(image_file, str(voter_image)[1:], 
                            model_name = self.models[1], distance_metric = self.metrics[2])
        return data
